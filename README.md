
# 🌐 WebScraper

A powerful Python-based tool for discovering subdomains and recursively crawling paths within a target domain.

---

## 🛠️ Features

- **Automatic Subdomain Enumeration**
  - Uses [crt.sh](https://crt.sh/) as a data source via Certificate Transparency logs.
  - Supports recursive subdomain discovery with configurable depth.

- **Recursive Path Crawling**
  - Finds internal paths by parsing HTML links (`<a>` tags).
  - Supports crawling to multiple depth levels.
  - Allows domain filtering and exclusion lists.

- **Domain Normalization**
  - Automatically cleans and standardizes URLs.
  - Removes fragments and "www." prefixes for consistency.

- **Colorful Banner & Logging**
  - Displays a clear CLI banner for better user experience.
  - Detailed console logs to track progress.

- **Export Functionality**
  - Save discovered subdomains and paths to `.txt` files.

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/WebScraper.git
cd WebScraper
pip install -r requirements.txt
```

**Dependencies:**
- `requests`
- `beautifulsoup4`

---

## 🚀 Usage

```bash
python webscraper.py -u example.com --subdomain --path
```

### Options

| Parameter         | Description                                      | Example                            |
|-------------------|--------------------------------------------------|------------------------------------|
| `-u`, `--url`     | Target domain (multiple domains separated by commas) | `-u example.com,example.org`  |
| `-f`, `--filter`  | Domains to exclude                               | `-f test.com,dev.example.com` |
| `--subdomain`     | Enable subdomain enumeration                     |                                    |
| `--path`          | Enable path crawling                              |                                    |

---

### Examples

#### Subdomain enumeration only

```bash
python webscraper.py -u example.com --subdomain
```

#### Path crawling (with or without subdomains)

```bash
python webscraper.py -u example.com --path
python webscraper.py -u example.com --subdomain --path
```

---

## 💾 Saving results

After the scan, you will be prompted to save results:

- **WebScraper_Subdomains.txt**: Contains all discovered subdomains.
- **WebScraper_Paths.txt**: Contains all discovered paths.

---

## ⚠️ Disclaimer

This tool is intended **for educational and authorized security testing purposes only**. Unauthorized scanning or crawling of systems without explicit permission is **illegal**.

---

## ✉️ Contact

Developed by **Dustin** (2025).

Feel free to open issues or submit pull requests for feedback, feature requests, or contributions.

---

## ⭐ Support

If you find this project helpful, please give it a ⭐!
