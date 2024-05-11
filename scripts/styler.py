class Styler:
    def boxify(self, headers):
        lines = headers.split("\n")
        max_length = max(len(line) for line in lines)
        border = f'╭{"─" * (max_length + 2)}╮'
        print(border)
        for line in lines:
            print(f"│ {line.ljust(max_length)} │")
        print(f'╰{"─" * (max_length + 2)}╯')
