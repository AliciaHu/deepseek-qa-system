import unittest
import asyncio
from core.response_gen import ResponseGenerator

class TestResponseGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """在所有测试开始前运行一次"""
        cls.qa_system = ResponseGenerator()

    def test_generate(self):
        """测试同步生成回答"""
        question = "今天天气怎么样？"
        response, gen_time = self.qa_system.generate(question)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        self.assertIsInstance(gen_time, float)
        self.assertGreater(gen_time, 0)

    def test_async_generate(self):
        """测试异步生成回答"""
        question = "今天天气怎么样？"
        loop = asyncio.get_event_loop()
        response, gen_time = loop.run_until_complete(self.qa_system.async_generate(question))
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        self.assertIsInstance(gen_time, float)
        self.assertGreater(gen_time, 0)

if __name__ == "__main__":
    unittest.main()
