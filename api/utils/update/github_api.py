import requests

def get_latest_release(owner, repo, token, logger):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tag_name = response.json()["tag_name"]
        logger.info(f"Latest release tag: {tag_name}")
        return tag_name
    except requests.exceptions.RequestException as e:
        logger.error("ERROR_REQUEST_FAILURE")
        raise Exception("ERROR_REQUEST_FAILURE") from e

def get_latest_hotfix(owner, repo, token, logger):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        releases = response.json()

        # Filter releases with tags that start with "hotfix"
        hotfix_releases = [release for release in releases if release["tag_name"].startswith("hotfix")]

        # Sort releases by release date (from latest to oldest)
        hotfix_releases.sort(key=lambda release: release["published_at"], reverse=True)

        if hotfix_releases:
            latest_hotfix_tag = hotfix_releases[0]["tag_name"]
            logger.info(f"Latest hotfix tag: {latest_hotfix_tag}")
            return latest_hotfix_tag
        else:
            logger.info("No hotfixes released")
            return None

    except requests.exceptions.RequestException as e:
        logger.error("ERROR_REQUEST_FAILURE")
        raise Exception("ERROR_REQUEST_FAILURE") from e
