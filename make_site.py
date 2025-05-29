import yaml
import os
from datetime import datetime

def format(html):
    return html.replace('arxiv', 'arXiv')

def read_yaml(file_path):
    """Read YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_html(projects, author_websites):
    """Generate HTML based on YAML data."""
    html = ""

    for project_key, project in projects.items():
        print(f"Processing project: {project_key}")
        title = project.get('title')
        if not title:
            print(f"WARNING: Project '{project_key}' has no title. Skipping.")
            continue

        thumbnail = project.get('thumbnail', '')
        authors = project.get('authors', [])
        venue = project.get('venue', '')
        year = project.get('year', '')
        description = project.get('description', '')
        links = project.get('links', {})
        paper_link = links.get('paper', '')

        html += f'''
    <tr>
      <td style="padding:20px;width:25%;vertical-align:middle">'''
        if thumbnail:
            html += f'''
        <img src="{thumbnail}" alt="{project_key}_png" style="border-style: none">'''
        html += '''
      </td>
      <td width="75%" valign="middle">'''

        if paper_link:
            html += f'''
        <a href="{paper_link}">
          <span class="papertitle">{title}</span>
        </a>'''
        else:
            html += f'''
        <span class="papertitle">{title}</span>'''

        html += '<br>'

        # Add authors with links
        authors_html = []
        for author in authors:
            if author == "Eric Xing":
                authors_html.append(f'<strong>{author}</strong>')
            elif author in author_websites and author_websites[author]:
                authors_html.append(f'<a href="{author_websites[author]}">{author}</a>')
            else:
                authors_html.append(author)
                print(f"WARNING: No website found for author '{author}'")

        html += ',\n        '.join(authors_html)

        if venue or year:
            html += f'<br>\n        <em>{venue}</em>'
            if venue and year:
                html += ', '
            html += f'{year}'

        # Add links
        links_html = []
        for link_type, link_url in links.items():
            if link_url:
                links_html.append(f'<a href="{link_url}">{link_type}</a>')
        if links_html:
            html += '<br>\n        ' + ' /\n        '.join(links_html)

        # Embed vLab link if applicable
        if 'vlab_url' in project and 'vLab' in description:
            vlab_position = description.find('vLab')
            if vlab_position != -1:
                prefix = description[:vlab_position]
                suffix = description[vlab_position + 4:]
                vlab_url = project['vlab_url']
                description = f"{prefix}<a href=\"{vlab_url}\">vLab</a>{suffix}"

        if description:
            html += f'''
        <p>{description}</p>'''

        html += '''
      </td>
    </tr>
'''
    return format(html)

def main():
    try:
        projects = read_yaml('./data/research/projects.yaml')
        author_websites_data = read_yaml('./data/research/author_websites.yaml')
        author_websites = author_websites_data.get('author_websites', {})

        body_html = generate_html(projects, author_websites)

        with open('./index_head.html', 'r') as file:
            head_html = file.read()
        with open('./index_foot.html', 'r') as file:
            foot_html = file.read()

        html = head_html + body_html + foot_html

        backup_dir = './legacy'
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, f'index_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')

        if os.path.exists('./index.html'):
            os.rename('./index.html', backup_file)

            legacy_files = sorted(os.listdir(backup_dir), key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
            if len(legacy_files) > 10:
                for file in legacy_files[:-5]:
                    os.remove(os.path.join(backup_dir, file))
                    print(f"Removed old backup file: {file}")

        with open('./index.html', 'w') as file:
            file.write(html)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
