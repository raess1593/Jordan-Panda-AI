from scrapers.nike_scraper import nike_scrap

def main():
    scrap_functs = [
        nike_scrap
    ]

    for funct in scrap_functs:
        funct()

if __name__ == "__main__":
    main()