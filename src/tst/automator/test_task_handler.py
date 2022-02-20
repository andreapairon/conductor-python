import multiprocessing
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.sample.simple_python_worker import SimplePythonWorker
from unittest.mock import MagicMock, Mock, patch
import unittest


class PickableMock(Mock):
    def __reduce__(self):
        return (Mock, ())


class TestTaskHandler(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_initialization_with_invalid_workers(self):
        expected_exception = Exception('Invalid worker list')
        with self.assertRaises(Exception) as context:
            TaskHandler(
                configuration=Configuration(),
                workers=SimplePythonWorker()
            )
            self.assertEqual(expected_exception, context.exception)

    def test_start(self):
        with patch.object(TaskRunner, 'run', PickableMock(return_value=None)):
            with self.__get_valid_task_handler() as task_handler:
                task_handler.start()
                self.assertEqual(len(task_handler.task_runner_processes), 1)
                for process in task_handler.task_runner_processes:
                    self.assertTrue(
                        isinstance(process, multiprocessing.Process)
                    )

    def __get_valid_task_handler(self):
        return TaskHandler(
            configuration=Configuration(),
            workers=[SimplePythonWorker()]
        )