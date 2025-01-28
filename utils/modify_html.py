from bs4 import BeautifulSoup


def modify_html(config):
    # Read the HTML file
    with open('webview.html', 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Update title
    title_tag = soup.find('title')
    if not title_tag:
        title_tag = soup.new_tag('title')
        soup.head.append(title_tag)
    title_tag.string = config['html']['title']

    # Update or add favicon
    favicon = soup.find('link', rel='icon')
    if not favicon:
        favicon = soup.new_tag('link', rel='icon', type='image/x-icon')
        # Insert favicon after meta tags
        meta_tags = soup.find_all('meta')
        if meta_tags:
            meta_tags[-1].insert_after(favicon)
        else:
            soup.head.insert(0, favicon)
    favicon['href'] = config['html']['favicon']
    favicon['type'] = 'image/x-icon'

    # Update or add theme CSS
    theme_link = soup.find('link', href=lambda x: x and 'theme' in x)
    if not theme_link:
        theme_link = soup.new_tag('link', rel='stylesheet', type='text/css')
        soup.head.append(theme_link)
    theme_link['href'] = config['html']['theme']
    theme_link['rel'] = 'stylesheet'
    theme_link['type'] = 'text/css'

    # Write the modified HTML
    with open(config['html']['filename'], 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
