import csv
import os


def clean_url(url):
    return url.strip() if isinstance(url, str) else ""


def get_social_icon(url):
    if "linkedin.com" in url:
        return "\\faLinkedin"
    elif "twitter.com" in url or "x.com" in url:
        return "\\faTwitter"
    elif "youtube.com" in url:
        return "\\faVideo"
    else:
        return "\\faGithub"


# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the root directory
root_dir = os.path.dirname(script_dir)
# Path to the CSV file
csv_path = os.path.join(root_dir, "AC-bo-hackathon-2024.csv")

# Load the CSV file
table_content = ""
unique_projects = set()

def project_sort_key(row):
    """Sort by numeric project number so the table is always ordered 1..N."""
    try:
        return (0, int(str(row.get("Project num", "")).strip()))
    except (TypeError, ValueError):
        return (1, str(row.get("Project num", "")))


try:
    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Sort by project number so appended rows appear in numeric order
    rows.sort(key=project_sort_key)

    # Iterate over each row in the CSV
    for row in rows:
            project_name = row["Project Name"]
            if project_name in unique_projects:
                continue  # Skip this row if the project name repeats

            unique_projects.add(project_name)
            project_num = row["Project num"]
            project_name_escaped = project_name.replace("&", "\\&")
            github_repo = clean_url(row["Github Repo"])
            social_media = clean_url(row["Link to Social Media Post"])
            video_link = clean_url(row["Link to Video (if recorded)"])

            links = []
            if github_repo:
                links.append(f"\\href{{{github_repo}}}{{\\faGithub}}")
            if social_media:
                links.append(
                    f"\\href{{{social_media}}}{{{get_social_icon(social_media)}}}"
                )
            if video_link:
                links.append(f"\\href{{{video_link}}}{{\\faVideo}}")

            links_str = " \\, ".join(links)  # Separate links with a small space

            table_content += (
                f"{project_num} & {project_name_escaped} & {links_str} \\\\\n"
            )
except FileNotFoundError:
    table_content = "% CSV file not found at " + csv_path + "\n"
    table_content += "% Providing empty table to allow compilation\n"
    table_content += "% Please make sure the CSV file exists\n"
    table_content += "\\multicolumn{3}{c}{CSV data not available} \\\\\n"

print(table_content)
