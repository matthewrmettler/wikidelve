
"""
Helper classes and methods.
"""

import logging
import requests

WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'


def fetch_wikipedia_pages_info(page_ids) -> dict:
  """Fetched page information such as title, URL, and image thumbnail URL for the provided page IDs.
  Args:
    page_ids: The page ids to process.
  Returns:
    Dict
  """
  print("fetch_wikipedia_pages_info(%s)" % page_ids)
  pages_info = {}

  current_page_ids_index = 0
  while current_page_ids_index < len(page_ids):
    # Query at most 50 pages per request (given WikiMedia API limits)
    end_page_ids_index = min(current_page_ids_index + 50, len(page_ids))

    query_params = {
        'action': 'query',
        'format': 'json',
        'pageids': '|'.join(page_ids[current_page_ids_index:end_page_ids_index]),
        'prop': 'info|pageimages|pageterms|categories|linkshere',
        'inprop': 'url|displaytitle',
        'piprop': 'thumbnail',
        'pithumbsize': 160,
        'pilimit': 50,
        'cllimit': 500,
        'lhlimit': 500,
        'wbptterms': 'description',
    }

    current_page_ids_index = end_page_ids_index

    # Identify this client as per Wikipedia API guidelines.
    # https://www.mediawiki.org/wiki/API:Main_page#Identifying_your_client
    headers = {
        'User-Agent': 'WikiDelve Project; matthewrmettler@gmail.com)',
    }

    req = requests.get(WIKIPEDIA_API_URL, params=query_params, headers=headers)

    try:
      pages_result = req.json().get('query', {}).get('pages')
    except ValueError as error:
      # Log and re-raise the exception.
      logging.exception({
          'error': 'Failed to decode MediaWiki API response: "{0}"'.format(error),
          'status_code': req.status_code,
          'response_text': req.text,
      })
      raise error

    for page_id, page in pages_result.items():
      page_id = int(page_id)

      if 'missing' in page:
        page_title = "MISSING"
        pages_info[page_id] = {
            'title': page_title,
            'url': 'https://en.wikipedia.org/wiki/{0}'.format(page_title)
        }
      else:
        pages_info[page_id] = {
            'title': page['title'],
            'url': page['fullurl']
        }

        thumbnail_url = page.get('thumbnail', {}).get('source')
        if thumbnail_url:
          pages_info[page_id]['thumbnailUrl'] = thumbnail_url

        description = page.get('terms', {}).get('description', [])
        if description:
          pages_info[page_id]['description'] = description[0][0].upper() + description[0][1:]

        categories = page.get('categories', [])
        if categories:
            cat_list = list()
            for c in categories:
                cat_list.append(c.get('title', '').replace("Category:", ""))
            pages_info[page_id]['categories'] = cat_list

        pages_info[page_id]['associations'] = page.get('linkshere', [])
              
  return pages_info

