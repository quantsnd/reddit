from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

# Dataframe and return data
redditFrame = []
nFrames = 0


# API Calls
@app.get("/")
def read_root():
    raise HTTPException(status_code=404, detail="Invalid request url")


@app.post("/subreddits")
def add_subreddit(subreddit: str):
    global redditFrame
    global nFrames
    subDict = {}
    id = nFrames
    nFrames += 1

    subDict['id'] = id
    subDict['Title'] = subreddit
    subDict['Posts'] = []
    subDict['number'] = 0
    redditFrame.append(subDict)

    return subDict


@app.put("/subreddits/{subreddit_id}")
def add_post(subreddit_id: int, post: str, post_metadata: str):
    global redditFrame
    postDict = {}
    index = search_by_subreddit_id(subreddit_id)
    subreddit = redditFrame[index]

    if subreddit:
        postDict['id'] = subreddit['number']
        postDict['Title'] = post
        postDict['Data'] = post_metadata
        redditFrame[index]['Posts'].append(postDict)
        redditFrame[index]['number'] += 1
        return postDict
    else:
        raise HTTPException(status_code=404, detail="Subreddit not found")


@app.get("/subreddits/{subreddit_id}")
def read_song(subreddit_id: int):
    global redditFrame
    index = search_by_subreddit_id(subreddit_id)
    subreddit = redditFrame[index]

    return {"id": subreddit["id"], "Title": subreddit["Title"], "Posts": subreddit["Posts"],
            "Number": subreddit["Number"]}


@app.get("/subreddits/{subreddit_id}/posts/{post_id}")
def read_song_title(subreddit_id: int, post_id: int):
    global redditFrame
    subredditIndex = search_by_subreddit_id(subreddit_id)
    subreddit = redditFrame[subredditIndex]
    post = subreddit[search_by_post_id(subreddit_id, post_id)]

    return {"id": post["id"], "Title": post["Title"], "Data": post["Data"]}


@app.delete("/subreddits/{subreddit_id}", status_code=200)
def delete_song(subreddit_id: int):
    global redditFrame
    redditFrame.pop(search_by_subreddit_id(subreddit_id))


@app.delete("/subreddits/{subreddit_id}/posts/{post_id}", status_code=200)
def delete_song(subreddit_id: int, post_id: int):
    global redditFrame
    postIndex = search_by_post_id(subreddit_id, post_id)
    redditFrame[subreddit_id]['Posts'].pop(postIndex)


def search_by_subreddit_title(title):
    global redditFrame
    lookupIndices = [lookupIndex for lookupIndex, subreddit in enumerate(redditFrame) if subreddit["Title"] == title]
    return lookupIndices


def search_by_subreddit_id(id):
    global redditFrame

    # lookup the ID
    lookupIndex = next((lookupIndex for lookupIndex, subreddit in enumerate(redditFrame) if subreddit["id"] == id), -1)

    if lookupIndex == -1:
        raise HTTPException(status_code=404, detail="id not found")
    else:
        return lookupIndex


def search_by_post_id(subreddit_id, post_id):
    global redditFrame

    # lookup the ID
    lookupIndex = next(
        (lookupIndex for lookupIndex, subreddit in enumerate(redditFrame) if subreddit["id"] == subreddit_id), -1)
    postIndex = next(
        (postIndex for postIndex, post in enumerate(redditFrame[lookupIndex]['Posts']) if post["id"] == post_id), -1)

    if postIndex == -1:
        raise HTTPException(status_code=404, detail="id not found")
    else:
        return postIndex
