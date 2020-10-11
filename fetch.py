import os
import sys
import googleapiclient.discovery


def main():
    url = sys.argv[1]
    try:
        fetch_count = int(sys.argv[2])
    except IndexError:
        fetch_count = 500


    perPage = 100

    videoId = url.split('v=')[1].split('&')[0]

    nextPageToken = 'initial'

    allComments = list()
    comments = list()
    times = fetch_count/perPage

    i = 0

    while nextPageToken and i < times:
        comments, nextPageToken = getComments(
            perPage, videoId, nextPage=nextPageToken)
        allComments.extend(comments)
        i = i + 1

    print("\n\n ".join(allComments))


def getComments(perPage, videoId, nextPage=None):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCMV0mcZa5eKnKVTu7C14wYW8iPIwNbX_g"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    if nextPage and nextPage != 'initial':
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=videoId,
            maxResults=perPage,
            pageToken=nextPage
        )
    else:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=videoId,
            maxResults=perPage,
        )

    response = request.execute()

    if response.get('nextPageToken') is None:
        nextPageToken = None
    else:
        nextPageToken = response['nextPageToken']

    comments = list()
    for item in response['items']:
        comments.append(item['snippet']['topLevelComment']
                        ['snippet']['textOriginal'])

    return comments, nextPageToken


if __name__ == "__main__":
    main()
