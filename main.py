import pytest
import datetime
import schedule
import time
import subprocess
import sys
import requests
import json
import urllib3
import os
import socket
import yaml
from bs4 import BeautifulSoup
from threading import Thread

# 禁用 SSL 警告（仅限测试环境）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def send_to_wecom(text, wecom_webhook_url):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": text,
            "mentioned_mobile_list": []
        }
    }
    try:
        response = requests.post(
            wecom_webhook_url,
            headers=headers,
            json=data,
            verify=False  # False忽略ssl警告
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"发送消息到企微失败: {str(e)}")
        return False


def start_allure_server(allure_results_dir, port=8080):
    # Allure 实际路径
    ALLURE_PATH = "C:\\Program Files\\Java\\allure-2.33.0\\bin\\allure.bat"

    allure_process = subprocess.Popen(
        [ALLURE_PATH, "serve", allure_results_dir, "--port", str(port), "--host", "0.0.0.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True  # Windows 需要 shell=True
    )
    print(f"Allure 服务启动，地址: {f'http://{socket.gethostbyname(socket.gethostname())}:{port}'}")
    return f"http://{socket.gethostbyname(socket.gethostname())}:{port}", allure_process


def count_test_cases(test_folder):
    test_count = 0
    for root, dirs, files in os.walk(test_folder):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        yaml_data = yaml.safe_load(f)
                        if isinstance(yaml_data, list):
                            for item in yaml_data:
                                if 'testcaseid' in item:
                                    test_count += 1
                        elif isinstance(yaml_data, dict) and 'testcaseid' in yaml_data:
                            test_count += 1
                except Exception as e:
                    print(f"读取 {file_path} 时出错: {e}")
    return test_count


def count_passed_and_failed_tests(allure_results_dir):
    passed_count = 0
    failed_count = 0
    skipped_count = 0
    if os.path.exists(allure_results_dir):
        for root, dirs, files in os.walk(allure_results_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if file.endswith('.json'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            status = data.get('status')
                            if status == 'passed':
                                passed_count += 1
                            elif status in ['failed', 'broken']:
                                failed_count += 1
                            elif status == 'skipped':
                                skipped_count += 1
                    elif file.endswith('.html'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                            soup = BeautifulSoup(html_content, 'html.parser')
                            text = soup.get_text()
                            if "Test Passed" in text:
                                passed_count += 1
                            elif "Test Failed" in text:
                                failed_count += 1
                            elif "Test Skipped" in text:
                                skipped_count += 1
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if "PASSED" in content:
                                passed_count += 1
                            elif "FAILED" in content:
                                failed_count += 1
                            elif "SKIPPED" in content:
                                skipped_count += 1
                except Exception as e:
                    print(f"读取 {file_path} 时出错: {e}")
    return passed_count, failed_count, skipped_count


def run_selected_tests(wecom_webhook_url):
    log_file = "task_log.txt"
    start_time = datetime.datetime.now()
    start_msg = f"定时任务在 {start_time} 开始执行"

    with open(log_file, "a", encoding='utf-8') as f:
        f.write(start_msg + "\n")

    # 清理 allure-results 目录
    allure_results_dir = "allure_results"
    if os.path.exists(allure_results_dir):
        for root, dirs, files in os.walk(allure_results_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    test_folder = "D:\\afsafafafafafafsfsf\\DCProject\\tests"
    total_tests = count_test_cases(test_folder)

    try:
        # 运行 pytest 测试并生成Allure报告数据
        result = subprocess.run(
            ["pytest", test_folder, "--alluredir=allure_results"],
            capture_output=True, text=True, encoding='utf-8', check=False
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout,
                                                stderr=result.stderr)

        passed_tests, failed_tests, skipped_tests = count_passed_and_failed_tests(allure_results_dir)

        # 启动Allure服务并获取URL
        report_url, allure_process = start_allure_server("allure_results")

        end_time = datetime.datetime.now()
        success_msg = (f"测试执行成功，耗时: {(end_time - start_time).total_seconds():.2f}秒\n"
                       f"测试总数: {total_tests}\n"
                       f"测试成功数量: {passed_tests}\n"
                       f"测试失败数量: {failed_tests}\n"
                       f"测试跳过数量: {skipped_tests}\n"
                       f"测试报告地址: {report_url}")

        with open(log_file, "a", encoding='utf-8') as f:
            f.write(success_msg + "\n")

        # 发送成功通知
        send_to_wecom(success_msg, wecom_webhook_url)

        # 保持Allure服务运行一段时间(如10分钟)
        time.sleep(600)
        allure_process.terminate()

    except subprocess.CalledProcessError as e:
        error_msg = f"测试执行失败: {str(e)}\n标准输出: {e.output}\n标准错误: {e.stderr}"
        print(error_msg)
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(error_msg + "\n")
        send_to_wecom(error_msg, wecom_webhook_url)


if __name__ == "__main__":
    WECOM_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2b2f77f3-cebe-4e93-bb52-8341d68725ae"

    # 立即运行一次
    run_selected_tests(WECOM_WEBHOOK_URL)

    # 定时任务
    schedule.every(2).minutes.do(run_selected_tests, WECOM_WEBHOOK_URL)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n定时任务已停止")