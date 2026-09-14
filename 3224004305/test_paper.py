import unittest
import tempfile
import os
import sys
from unittest.mock import patch
from main import preprocess, ngram_segment, calc_similarity, read_file, write_answer, main


class TestCalcModule(unittest.TestCase):
    # ========== 预处理函数测试 ==========
    # 预处理-正常文本测试
    def test_preprocess_normal(self):
        res = preprocess("今天天气真好！Hello 123，测试文本。")
        self.assertEqual(res, "今天天气真好Hello123测试文本")

    # 预处理-全标点测试
    def test_preprocess_only_punct(self):
        res = preprocess("，。！？；：、")
        self.assertEqual(res, "")

    # 预处理-空字符串测试
    def test_preprocess_empty(self):
        res = preprocess("")
        self.assertEqual(res, "")

    # 预处理-仅空白符测试
    def test_preprocess_blank(self):
        res = preprocess("   \n\t   ")
        self.assertEqual(res, "")

    # ========== n-gram分词函数测试 ==========
    # ngram-正常分词测试
    def test_ngram_normal(self):
        res = ngram_segment("abcdef", n=2)
        self.assertEqual(res, {"ab", "bc", "cd", "de", "ef"})

    # ngram-文本长度等于窗口值
    def test_ngram_equal_len(self):
        res = ngram_segment("你好", n=2)
        self.assertEqual(res, {"你好"})

    # ngram-文本长度小于窗口值
    def test_ngram_short_text(self):
        res = ngram_segment("你", n=2)
        self.assertEqual(res, set())

    # ngram-非法参数n=0（异常场景）
    def test_ngram_zero_n(self):
        with self.assertRaises(ValueError):
            ngram_segment("测试文本", n=0)

    # ========== 相似度计算函数测试 ==========
    # 相似度-完全相同文本
    def test_calc_same_text(self):
        a = {"ab", "bc", "cd"}
        b = {"ab", "bc", "cd"}
        self.assertAlmostEqual(calc_similarity(a, b), 1.0)

    # 相似度-完全无关文本
    def test_calc_no_same(self):
        a = {"ab", "bc"}
        b = {"xy", "yz"}
        self.assertEqual(calc_similarity(a, b), 0.0)

    # 相似度-部分重合文本
    def test_calc_part_same(self):
        a = {"ab", "bc", "cd"}
        b = {"bc", "cd", "de"}
        self.assertAlmostEqual(calc_similarity(a, b), 0.5)

    # 相似度-空集防除零崩溃
    def test_calc_empty_set(self):
        self.assertEqual(calc_similarity(set(), set()), 0.0)

    # ========== IO函数测试 ==========
    # 测试read_file读取文件
    def test_read_file(self):
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
            f.write("测试文本123")
            tmp_path = f.name
        try:
            res = read_file(tmp_path)
            self.assertEqual(res, "测试文本123")
        finally:
            os.unlink(tmp_path)

    # 测试write_answer写入结果
    def test_write_answer(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp_path = f.name
        try:
            write_answer(tmp_path, 0.75)
            content = read_file(tmp_path)
            self.assertEqual(content, "重复率：0.75")
        finally:
            os.unlink(tmp_path)

    # ========== main入口函数测试 ==========
    # 测试main函数：参数数量不对分支
    @patch("sys.argv", ["main.py"])
    def test_main_wrong_arg_count(self):
        main()

    # 测试main函数：正常执行逻辑（mock掉IO，不真实读写文件）
    @patch("main.write_answer")
    @patch("main.read_file", side_effect=["文本A", "文本B"])
    def test_main_normal_run(self, mock_read, mock_write):
        sys.argv = ["main.py", "f1.txt", "f2.txt", "out.txt"]
        main()
        mock_write.assert_called_once()


if __name__ == '__main__':
    unittest.main()
