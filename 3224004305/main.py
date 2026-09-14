import sys
import re

def parse_argv():
    """
    解析命令行参数
    返回：(原文路径,抄袭版路径,输出路径)
    参数数量不对则提示并退出
    """
    if len(sys.argv) != 4:
        print("参数错误！用法：python main.py 原文绝对路径 抄袭版绝对路径 输出文件绝对路径")
        sys.exit(0)
    orig_path = sys.argv[1]    # 原文文件路径
    copy_path = sys.argv[2]    # 抄袭版文件路径
    out_path = sys.argv[3]     # 结果输出路径
    return orig_path, copy_path, out_path


def read_file(file_path):
    """
    读取文件，自动尝试utf‑8、gbk编码
    返回文本字符串；发生异常返回None
    """
    encodings = ["utf-8", "gbk"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()   # 一次性读取全部文本
            return content
        except FileNotFoundError:
            print(f"错误：找不到文件 {file_path}")
            return None
        except UnicodeDecodeError:
            continue    # 当前编码失败，尝试下一种编码
        except Exception as e:
            print(f"读取文件异常 {file_path}，{e}")
            return None
    print(f"文件 {file_path} 编码解析失败")
    return None


def preprocess(text: str):
    """
    文本预处理
    去除换行、空格，过滤全部标点符号，只保留中文字符
    """
    # 去掉换行、空格
    text = text.replace("\n", "").replace(" ", "")
    # 只保留中文字符
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    text = pattern.sub("", text) # 将非中文字符替换为空
    return text


def ngram_segment(text: str, n: int):
    """
    n‑gram滑动窗口分词
    :param text:预处理之后的文本
    :param n:窗口大小，本项目使用n=2
    :return:所有n元片段的集合
    """
    seg_set = set()
    text_len = len(text)
    if text_len < n:    # 文本长度不足窗口大小，直接返回空集合
        return seg_set
    for i in range(text_len - n + 1):
        seg = text[i:i + n]  # 截取连续n个字的片段
        seg_set.add(seg)     # 加入集合自动去重
    return seg_set


def calc_similarity(orig_text: str, copy_text: str, n=2):
    """
    计算论文重复率
    公式：重复率 = 交集片段数量 / 抄袭版总片段数量
    边界：抄袭文本过短返回0.0，避免除零
    """
    orig_set = ngram_segment(orig_text, n)      # 原文2-gram分词
    copy_set = ngram_segment(copy_text, n)     # 抄袭版2-gram分词
    # 边界保护，抄袭版没有足够片段直接返回0
    if len(copy_set) == 0:
        return 0.0
    inter_set = orig_set.intersection(copy_set) # 获取两个集合交集
    repeat_rate = len(inter_set) / len(copy_set)# 计算重复率
    return repeat_rate


def write_answer(out_path: str, rate: float):
    """
    将重复率保留小数点后两位写入输出文件
    """
    output_str = "{:.2f}".format(rate) # 格式化，保留两位小数
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output_str) # 将结果写入文件
        print(f"计算完成，重复率：{output_str}，结果写入{out_path}")
    except Exception as e:
        print(f"写入输出文件失败：{e}")


def main():
    """程序总调度入口"""
    orig_path, copy_path, out_path = parse_argv() # 获取三个文件路径
    orig_content = read_file(orig_path)           # 读取原文内容
    copy_content = read_file(copy_path)           # 读取抄袭版内容
    # 文件读取失败直接结束
    if orig_content is None or copy_content is None:
        return
    orig_clean = preprocess(orig_content)    # 原文预处理清洗
    copy_clean = preprocess(copy_content)     # 抄袭版预处理清洗
    repeat_rate = calc_similarity(orig_clean, copy_clean) # 计算重复率
    write_answer(out_path, repeat_rate)      # 写入结果文件


if __name__ == "__main__":
    main() # 启动程序
