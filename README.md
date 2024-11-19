
# Python RSS Reader

A **command-line RSS reader** built with Python 3.10, designed to parse RSS 2.0 feeds, output them in **JSON** or formatted **plain text**, and limit the number of news items displayed.

This project was reuploaded from [this GitLab repository](https://gitlab.com/42plat0/scrapper-student-template) and passes all provided tests, including support for RSS feeds in plain text, JSON output, and online manipulation.

---

## Features

- Parses RSS 2.0 feeds with customizable formatting.
- Outputs:
  - **Console Output**: A structured plain-text representation of the feed and its items.
  - **JSON Output**: A well-formatted JSON representation of the feed with 2-space indentation.
- Supports **command-line arguments** for:
  - Fetching RSS feeds from the web.
  - Limiting the number of news items displayed.
  - Printing results in JSON format.
- Handles encoding issues (e.g., `&#39;` symbols) in both console and JSON outputs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rss-reader.git
   cd rss-reader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Usage

```bash
usage: rss_reader.py [-h] [--json] [--limit LIMIT] source

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     Show this help message and exit
  --json         Print result as JSON in stdout
  --limit LIMIT  Limit news topics if this parameter is provided
```

### Examples

#### Fetch and Display RSS Feed
```bash
python rss_reader.py "https://news.yahoo.com/rss"
```

#### Fetch RSS Feed and Output as JSON
```bash
python rss_reader.py --json "https://news.yahoo.com/rss"
```

#### Limit the Number of Items Displayed
```bash
python rss_reader.py --limit 5 "https://news.yahoo.com/rss"
```

---

## Console Output Format

### Channel Information
- `Feed: [Feed Title]`
- `Link: [Feed Link]`
- `Last Build Date: [Feed Last Build Date]`
- `Publish Date: [Feed Publish Date]`
- `Language: [Feed Language]`
- `Categories: [Category1], [Category2]`
- `Editor: [Managing Editor]`
- `Description: [Feed Description]`

### News Items
For each item:
- `Title: [News Title]`
- `Author: [News Author]`
- `Published: [News Publish Date]`
- `Link: [News Link]`
- `Categories: [Category1], [Category2]`
- `[News Description]` (on a new line)

Example:
```plaintext
Feed: Yahoo News - Latest News & Headlines
Link: https://news.yahoo.com/rss
Description: Yahoo news description

Title: Nestor heads into Georgia after tornados damage Florida
Published: Sun, 20 Oct 2019 04:21:44 +0300
Link: https://news.yahoo.com/wet-weekend-tropical-storm-warnings-131131925.html

Nestor raced across Georgia as a post-tropical cyclone late Saturday, hours after the former tropical storm spawned a tornado that damaged homes and a school in central Florida while sparing areas of the Florida Panhandle devastated one year earlier by Hurricane Michael.
```

---

## JSON Output Format

A JSON representation of the RSS feed is generated when using the `--json` flag. Example:
```json
{
  "title": "Yahoo News - Latest News & Headlines",
  "link": "https://news.yahoo.com/rss",
  "description": "Yahoo news description",
  "items": [
    {
      "title": "Nestor heads into Georgia after tornados damage Florida",
      "pubDate": "Sun, 20 Oct 2019 04:21:44 +0300",
      "link": "https://news.yahoo.com/wet-weekend-tropical-storm-warnings-131131925.html",
      "description": "Nestor raced across Georgia as a post-tropical cyclone late Saturday, hours after the former tropical storm spawned a tornado that damaged homes and a school in central Florida while sparing areas of the Florida Panhandle devastated one year earlier by Hurricane Michael."
    }
  ]
}
```
