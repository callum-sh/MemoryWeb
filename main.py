from utils.get_photos import service_account_login, get_all_photos
from utils.plot import construct_graph


def main():
    # Login to Google Photos
    creds = service_account_login()

    # Get all photos (limited to the first 100)
    photos = get_all_photos(creds)
    print(f'Found {len(photos)} photos')

    # Construct graph
    G = construct_graph(photos)
    print(
        f'Constructed graph with {len(G.nodes)} nodes and {len(G.edges)} edges')


if __name__ == "__main__":
    main()
