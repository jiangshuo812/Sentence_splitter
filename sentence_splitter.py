import os 

current_path = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_path)

import spacy
import json
from pathlib import Path
from typing import List, Dict
from loguru import logger
import docx
from spacy.language import Language

class SentenceSplitter:
    def __init__(self):
        """初始化SentenceSplitter类"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("成功加载spaCy模型")
        except OSError:
            logger.error("spaCy模型未找到，正在下载...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy模型下载完成")

    def read_text_file(self, file_path: str) -> str:
        """读取文本文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"读取文件时出错: {str(e)}")
            raise

    def read_docx_file(self, file_path: str) -> str:
        """读取Word文档内容"""
        try:
            doc = docx.Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            logger.error(f"读取Word文档时出错: {str(e)}")
            raise

    def split_sentences(self, text: str) -> List[str]:
        """将文本分割成句子"""
        try:
            doc = self.nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents]
            logger.info(f"成功分割出 {len(sentences)} 个句子")
            return sentences
        except Exception as e:
            logger.error(f"分割句子时出错: {str(e)}")
            raise

    def process_file(self, input_path: str, output_path: str) -> None:
        """处理输入文件并保存结果"""
        try:
            # 确定文件类型并读取内容
            input_path = Path(input_path)
            if input_path.suffix.lower() == '.docx':
                text = self.read_docx_file(str(input_path))
            else:
                text = self.read_text_file(str(input_path))

            # 分割句子
            sentences = self.split_sentences(text)

            # 构建输出数据
            output_data = {
                "total_sentences": len(sentences),
                "sentences": sentences
            }

            # 保存结果
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"结果已保存到 {output_path}")

        except Exception as e:
            logger.error(f"处理文件时出错: {str(e)}")
            raise

def main():
    # 配置日志
    logger.add("sentence_splitter.log", rotation="500 MB")
    
    try:
        splitter = SentenceSplitter()
        
        # 示例用法
        input_file = "test_1.txt"  # 或 "input.docx"
        output_file = "test_1_output.json"
        
        splitter.process_file(input_file, output_file)
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        raise

if __name__ == "__main__":
    main() 