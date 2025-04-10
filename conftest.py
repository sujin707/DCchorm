# import pytest
# import pytest_html
#
# def pytest_runtest_makereport(item, call):
#     # 直接从 call.excinfo 获取报告对象
#     report = call.excinfo.getrepr() if call.excinfo else None
#     if hasattr(report, 'wasxfail'):
#         return report
#     extra = getattr(report, 'extra', [])
#     if call.when == 'call':
#         # 检查测试用例的 testCaseId 是否正确
#         test_case_id = item.callspec.params.get('testCaseId')
#         if test_case_id:
#             extra.append(pytest_html.extras.text(f"testCaseId: {test_case_id}"))
#     if report:
#         report.extra = extra
#     return report