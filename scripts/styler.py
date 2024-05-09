class Styler:
    def boxify(self, headers):
        """
        Boxify the headers.

        Parameters:
            headers (str): The headers to boxify.

        Example:
            styler.boxify("Duplicate Images")
        """

        # Split the headers by newline
        lines = headers.split("\n")

        # Get the maximum length of the line
        max_length = max(len(line) for line in lines)

        # Create the box
        border = f'╭{"─" * (max_length + 2)}╮'
        print(border)

        # Print the headers
        for line in lines:
            print(f"│ {line.ljust(max_length)} │")

        # Close the box
        print(f'╰{"─" * (max_length + 2)}╯')
