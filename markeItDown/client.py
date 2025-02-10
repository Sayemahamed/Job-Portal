import requests
import os


def upload_file(
    file_path: str,
    output_dir: str = "converted_files",
    server_url: str = "http://localhost:8003/convert",
):
    """
    Uploads a file to the FastAPI service and saves the Markdown conversion result.

    :param file_path: Path to the file to be uploaded.
    :param output_dir: Directory where the converted Markdown file will be saved.
    :param server_url: The API endpoint for file conversion.
    """
    try:
        with open(file_path, "rb") as file:
            files = {
                "file": (os.path.basename(file_path), file, "application/octet-stream")
            }
            response = requests.post(server_url, files=files)

        # Raise an error if the request fails
        response.raise_for_status()

        # Get the converted Markdown text
        markdown_content = response.json().get("text_content", "")

        if markdown_content:
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Create an output file with the same name as the input but with .md extension
            output_file_path = os.path.join(
                output_dir, os.path.splitext(os.path.basename(file_path))[0] + ".md"
            )

            # Save the Markdown text to a file
            with open(output_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)

            print(f"Converted Markdown saved to: {output_file_path}")
        else:
            print("No content returned from server.")

    except requests.exceptions.RequestException as e:
        print("Error:", e)


# Example usage
if __name__ == "__main__":
    file_path = "C:\\Users\\sayem\\OneDrive\\Desktop\\Thesis_Proposal.pdf"
    upload_file(file_path)
