import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import patch
from amazon_android import vision
from amazon_android.core import ToolError


class ParallelOcrTests(unittest.TestCase):
    def test_two_readers_use_separate_engines_and_keep_results(self):
        barrier = threading.Barrier(2, timeout=2)
        used = set()
        def engine(slot):
            used.add(slot)
            def read(value):
                barrier.wait()
                return SimpleNamespace(boxes=None, txts=(value,), scores=None)
            return read
        with patch.object(vision, '_engine', side_effect=engine):
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(vision._recognize, name) for name in ('q1', 'q2')]
                self.assertEqual([f.result().txts for f in futures], [('q1',), ('q2',)])
        self.assertEqual(used, {0, 1})

    def test_stop_does_not_enter_ocr_and_releases_slot(self):
        stop = threading.Event(); stop.set()
        with patch.object(vision, '_engine') as engine:
            with self.assertRaises(ToolError):
                vision._recognize(None, stop=stop)
        engine.assert_not_called()
        self.assertEqual(vision._ocr_slots.qsize(), 2)

    def test_stop_during_recognition_discards_result_and_frees_engine(self):
        stop = threading.Event()
        def read(raw):
            stop.set()
            return SimpleNamespace(boxes=None, txts=('stale',), scores=None)
        with patch.object(vision, '_engine', return_value=read):
            with self.assertRaises(ToolError):
                vision._recognize(None, stop=stop)
        self.assertEqual(vision._ocr_slots.qsize(), 2)

    def test_engine_failure_does_not_block_next_phone(self):
        with patch.object(vision, '_engine', side_effect=RuntimeError('reader failed')):
            with self.assertRaises(RuntimeError):
                vision._recognize(None)
        self.assertEqual(vision._ocr_slots.qsize(), 2)
