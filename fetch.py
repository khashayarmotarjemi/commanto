import os
import sys
import googleapiclient.discovery
from subprocess import run, Popen, PIPE, STDOUT
from rake_nltk import Rake


def main():
    url = sys.argv[1]
    fetch_count = int(sys.argv[2])

    video_id = url.split('v=')[1].split('&')[0]

    comments = get_all_comments(video_id, fetch_count)

    c = input('what action? (f: fzf, w: words): ')

    if c == 'f':
        comments_str = "\n\n".join(comments)

        fzf_p = run(['fzf'], stdout=PIPE,
                    input=comments_str, encoding='utf-8')
        print(fzf_p.stdout)

    elif c == 'w':
        # Uses stopwords for english from NLTK, and all puntuation characters.
        print(get_key_words(comments))


def get_key_words(comments):
    r = Rake()
    r.extract_keywords_from_sentences(comments)
    return r.get_ranked_phrases_with_scores()


def get_all_comments(video_id, fetch_count):
    per_page = 20

    if per_page > fetch_count:
        per_page = fetch_count

    if per_page > fetch_count:
        per_page = fetch_count

    next_page_token = 'initial'

    all_comments = list()
    comments = list()
    times = fetch_count/per_page
    i = 0

    while next_page_token and i < times:
        comments, next_page_token = get_comments(
            per_page, video_id, next_page=next_page_token)
        all_comments.extend(comments)
        i = i + 1

    return all_comments


def get_comments(per_page, video_id, next_page=None):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCMV0mcZa5eKnKVTu7C14wYW8iPIwNbX_g"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    if next_page and next_page != 'initial':
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=per_page,
            pageToken=next_page
        )
    else:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=per_page,
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
