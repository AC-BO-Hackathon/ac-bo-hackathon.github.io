import json
import os


def clean_text(text):
    import re
    # First escape other characters
    text = (
        text.replace("&", "\\&")
        .replace("%", "\\%")
        .replace("#", "\\#")
    )
    
    # Handle underscores carefully - don't escape them inside \cite{} commands
    # Use regex to find \cite{...} blocks and protect them
    def protect_citations(match):
        return match.group(0)  # Return citation as-is
    
    # Split text by citation blocks and process each part
    parts = re.split(r'(\\cite\{[^}]*\})', text)
    for i in range(len(parts)):
        if not parts[i].startswith('\\cite{'):
            # This is regular text, escape underscores
            parts[i] = parts[i].replace("_", "\\_")
    
    return ''.join(parts)


# def gen_summary(input_dir):
#     sections = []

#     for filename in os.listdir(input_dir):
#         if filename.endswith(".json"):
#             with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
#                 data = json.load(file)
#                 # project_number = clean_text(data.get("project_number", "Unknown Project"))
#                 project_name = clean_text(data.get("project_name", "Unknown Project"))
#                 summary = clean_text(data.get("summary", "No summary available."))
#                 video_url = data.get("video_url", "")

#                 if video_url:
#                     section_title = f"\\subsection*{{\\href{{{video_url}}}{{{project_name}}}}}"
#                 else:
#                     section_title = f"\\subsection*{{{project_name}}}"

#                 section = f"{section_title}\n\n{summary}\n"
#                 sections.append(section)

#     print(" ".join(sections))


def gen_summary(input_dir):
    # Check if directory exists
    if not os.path.exists(input_dir):
        return (
            "% JSON directory not found at: "
            + input_dir
            + "\n"
            + "\\subsection*{Project Summaries Not Available}\n\n"
            + "The project summaries will be available in the final version of the document. "
            + "Please ensure the JSON directory exists and contains the necessary files."
        )

    sections = []
    entries = []

    try:
        for filename in os.listdir(input_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as file:
                        data = json.load(file)
                        project_number = clean_text(
                            str(data.get("project_number", "Unknown Project"))
                        )
                        project_name = clean_text(data.get("project_name", "Unknown Project"))
                        summary = clean_text(data.get("summary", "No summary available."))
                        video_url = data.get("video_url", "")

                        entries.append((project_number, project_name, summary, video_url))
                except Exception as e:
                    sections.append(
                        f"\\subsection*{{Error Processing {filename}}}\n\nError: {e}\n"
                    )
    except Exception as e:
        return (
            f"% Error accessing JSON directory: {str(e)}\n"
            + "\\subsection*{Error Processing Summaries}\n\n"
            + f"An error occurred while processing the project summaries: {str(e)}"
        )

    # Sort entries by project number
    try:
        entries.sort(key=lambda x: int(x[0]))
    except ValueError:
        entries.sort(key=lambda x: x[0])

    # Generate sections
    for project_number, project_name, summary, video_url in entries:
        title = f"Project {project_number}: {project_name}"
        if video_url:
            section_title = f"\\subsection*{{\\href{{{video_url}}}{{{title}}}}}"
        else:
            section_title = f"\\subsection*{{{title}}}"

        section = f"{section_title}\n\n{summary}\n"
        sections.append(section)

    if not sections:
        return "\\subsection*{No Project Summaries Found}\n\nNo project summary files were found in the specified directory."

    return " ".join(sections)


# Get the script directory and project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Use absolute path for the JSON directory
local_json_dir = os.path.join(project_root, "_projects", "json_summaries")

# Generate and print the summaries
print(gen_summary(local_json_dir))
