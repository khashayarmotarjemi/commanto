import os
import sys
import googleapiclient.discovery

def main():

    url = sys.argv[1]

    videoId = url.split('v=')[1].split('&')[0]


    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCMV0mcZa5eKnKVTu7C14wYW8iPIwNbX_g"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=videoId,
        maxResults=200
    )
    response = request.execute()

    comments = list()
    for item in response['items']:
        comments.append(item['snippet']['topLevelComment']['snippet']['textOriginal'] )

    print ("\n\n ".join(comments))

if __name__ == "__main__":
    main()


    