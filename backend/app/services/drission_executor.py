from drissionpage import ChromiumPage

class DrissionExecutor:
    def __init__(self, headless: bool = True):
        self.page = ChromiumPage(headless=headless)

    def run_steps(self, steps: list):
        """
        执行用例步骤，steps 为操作步骤列表，每个步骤为 dict，如：
        {"action": "goto", "url": "https://www.baidu.com"}
        """
        results = []
        for step in steps:
            action = step.get('action')
            if action == 'goto':
                url = step.get('url')
                self.page.get(url)
                results.append(f"Goto {url}")
            elif action == 'click':
                selector = step.get('selector')
                self.page.ele(selector).click()
                results.append(f"Click {selector}")
            elif action == 'input':
                selector = step.get('selector')
                text = step.get('text')
                self.page.ele(selector).input(text)
                results.append(f"Input '{text}' to {selector}")
            # 可扩展更多操作
            else:
                results.append(f"Unknown action: {action}")
        return results 