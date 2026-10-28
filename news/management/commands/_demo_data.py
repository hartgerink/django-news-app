# Demo data
# ---------
# The sample accounts, publications, subscriptions, articles, and
# newsletters that seed_demo_data loads. This file holds only the
# data; the command decides how to load it.
#
# The pieces are linked by name: owners, staff, readers, subscribed
# journalists, and authors are usernames from USERS; publications are
# names from PUBLICATIONS; and a newsletter's articles are titles from
# ARTICLES.
#
# The underscore at the start of the file's name keeps Django from
# treating it as a command. Every other .py file in management/commands/
# becomes one. seed_demo_data, in the same folder, reads the data with:
#     from . import _demo_data as demo_data
#     demo_data.USERS  # the list of accounts

from accounts.models import User

# Every demo account uses this password.
PASSWORD = "newspaper"

# The demo accounts. Two of each role cover the usual situations, and a
# few more cover the rest:
#     "Jonah"   # a Journalist on the staff of both publications
#     "Jade"    # an independent Journalist, on no publication's staff
#     "Ezra"    # an Editor on the staff of both publications
#     "Esther"  # an Editor on no publication's staff
#     "Rosa"    # a Reader who subscribes to nothing
# Each account logs in with its username and the password above.
USERS = [
    {
        "username": "Paul",
        "role": User.PUBLISHER,
        "email": "paul@djangonews.local",
    },
    {
        "username": "Penny",
        "role": User.PUBLISHER,
        "email": "penny@djangonews.local",
    },
    {
        "username": "James",
        "role": User.JOURNALIST,
        "email": "james@djangonews.local",
    },
    {
        "username": "Julia",
        "role": User.JOURNALIST,
        "email": "julia@djangonews.local",
    },
    {
        "username": "Jonah",
        "role": User.JOURNALIST,
        "email": "jonah@djangonews.local",
    },
    {
        "username": "Jade",
        "role": User.JOURNALIST,
        "email": "jade@djangonews.local",
    },
    {
        "username": "Edward",
        "role": User.EDITOR,
        "email": "edward@djangonews.local",
    },
    {
        "username": "Elena",
        "role": User.EDITOR,
        "email": "elena@djangonews.local",
    },
    {
        "username": "Ezra",
        "role": User.EDITOR,
        "email": "ezra@djangonews.local",
    },
    {
        "username": "Esther",
        "role": User.EDITOR,
        "email": "esther@djangonews.local",
    },
    {
        "username": "Richard",
        "role": User.READER,
        "email": "richard@djangonews.local",
    },
    {
        "username": "Rhonda",
        "role": User.READER,
        "email": "rhonda@djangonews.local",
    },
    {
        "username": "Rosa",
        "role": User.READER,
        "email": "rosa@djangonews.local",
    },
]

# A superuser for the Django admin, with the same password.
SUPERUSER = {
    "username": "admin",
    "email": "admin@djangonews.local",
}

# The demo publications' names, also used in SUBSCRIPTIONS, ARTICLES,
# and NEWSLETTERS, so a typo raises an error instead of linking to a
# publication that does not exist.
GAZETTE = "The Lamplight Gazette"
COURIER = "The Copper Kettle Courier"

# The demo publications, one owned by each demo Publisher. Each has two
# editors and two journalists on its staff: its own pair, plus Ezra and
# Jonah, who work for both. The owner, editors, and journalists are
# usernames from USERS. For example:
#     "Paul"    # owns The Lamplight Gazette
#     "Elena"   # edits for The Lamplight Gazette
PUBLICATIONS = [
    {
        "name": GAZETTE,
        "owner": "Paul",
        "description": (
            "Evening news for night owls: city politics, late-breaking "
            "stories, and the people who keep the lights on."
        ),
        "editors": ["Elena", "Ezra"],
        "journalists": ["James", "Jonah"],
    },
    {
        "name": COURIER,
        "owner": "Penny",
        "description": (
            "Food, community, and small-town life, served warm every "
            "morning."
        ),
        "editors": ["Edward", "Ezra"],
        "journalists": ["Julia", "Jonah"],
    },
]

# What each demo Reader subscribes to. The two Readers subscribe to
# different things, so each one's subscribed articles differ. A
# subscription to a journalist covers only their independent articles,
# so Rhonda gets Julia's independent articles through her subscription
# to Julia, and Julia's Courier articles through her subscription to The
# Copper Kettle Courier. Rosa is not listed, so she subscribes to
# nothing. For example:
#     "Richard", GAZETTE  # Richard subscribes to The Lamplight Gazette
SUBSCRIPTIONS = [
    {
        "reader": "Richard",
        "publications": [GAZETTE],
        "journalists": ["Julia"],
    },
    {
        "reader": "Rhonda",
        "publications": [COURIER],
        "journalists": ["James", "Julia"],
    },
]

# The demo articles. James and Julia each write three for their own
# publication, two approved and one pending, plus two independent
# articles, one approved and one pending. Jonah writes for both
# publications, and Jade writes only independent articles. The author
# is a username from USERS, and publication is None for an independent
# article. days_ago sets how long ago the article was created, so the
# lists show different dates. For example:
#     "publication": GAZETTE  # filed under The Lamplight Gazette
#     "publication": None     # independent
#     "days_ago": 3           # created 3 days before the command ran
ARTICLES = [
    {
        "title": "Night Market Lanterns Return to Canal Street",
        "author": "James",
        "publication": GAZETTE,
        "approved": True,
        "days_ago": 12,
        "content": (
            "After a three-year absence, the paper lanterns of the Canal "
            "Street night market flickered back to life on Friday, strung "
            "between the old warehouses like a second, lower set of stars. By "
            "nine o'clock the line for Mr. Okafor's grilled corn stretched "
            "past the bridge, and a brass band that nobody remembered booking "
            "played until the police politely asked them to stop, then stayed "
            "to hear one more song. Organizers say the market will run every "
            "Friday until the first frost, or until the lanterns run out, "
            "whichever comes first."
        ),
    },
    {
        "title": "City Council Votes to Keep the Old Clock Tower Ticking",
        "author": "James",
        "publication": GAZETTE,
        "approved": True,
        "days_ago": 8,
        "content": (
            "In a late-night session that ran well past the hour the clock "
            "tower itself would have struck, the city council voted seven to "
            "two to repair the 140-year-old mechanism rather than replace it "
            "with a digital display. Councilor Marsh argued that a city "
            "should be able to hear what time it is, not just read it. The "
            "repairs will be carried out by a retired watchmaker who has "
            "volunteered his weekends, on the single condition that he be "
            "allowed to wind the clock himself every Sunday for the rest of "
            "his life."
        ),
    },
    {
        "title": "The Last Tram Driver on Route 9",
        "author": "James",
        "publication": GAZETTE,
        "approved": False,
        "days_ago": 2,
        "content": (
            "Every night at 11:52, Dolores Finch eases tram number 14 out of "
            "the depot for the final run of Route 9, a loop of the sleeping "
            "city that few riders ever see. Her regulars include two night "
            "nurses, a baker heading in to start the morning bread, and a "
            "gray cat that boards at Elm Square and rides exactly three "
            "stops. After twenty-six years behind the controls, Finch retires "
            "next month. She says she will miss the quiet most of all, and "
            "the cat, who has never once paid a fare."
        ),
    },
    {
        "title": "What the Fog Remembers",
        "author": "James",
        "publication": None,
        "approved": True,
        "days_ago": 15,
        "content": (
            "The fog came in off the river again last night, the thick kind "
            "that turns streetlights into dandelion clocks and swallows the "
            "sound of your own footsteps. Walking home through it, I passed a "
            "man reading a newspaper under a lamp, a couple arguing softly in "
            "two languages, and a dog who seemed to know exactly where he was "
            "going. By morning the fog had gone, taking all of them with it, "
            "and the street looked ordinary again. I have started to think "
            "the fog does not hide the city at all. It simply shows us the "
            "parts we are usually too busy to notice."
        ),
    },
    {
        "title": "A Field Guide to Insomniac Pigeons",
        "author": "James",
        "publication": None,
        "approved": False,
        "days_ago": 1,
        "content": (
            "Most pigeons go to bed at sunset, but a small and stubborn "
            "population near the central station has decided that the night "
            "is simply too interesting to miss. Over six weeks of careful "
            "observation, this reporter identified three distinct types: the "
            "Platform Patroller, who inspects every bench for crumbs; the "
            "Neon Admirer, who sits beneath the pharmacy sign for hours; and "
            "the rare Midnight Commuter, who boards the last train and gets "
            "off, apparently on purpose, at the airport. Scientists have no "
            "explanation. The pigeons declined to comment."
        ),
    },
    {
        "title": "Mrs. Abernathy's Scones Win the County Fair, Again",
        "author": "Julia",
        "publication": COURIER,
        "approved": True,
        "days_ago": 14,
        "content": (
            "For the eleventh year in a row, the blue ribbon for best baked "
            "good at the county fair went to Margaret Abernathy and her "
            "cheddar and chive scones, a recipe she insists contains nothing "
            "special at all. Rival bakers have tried everything from imported "
            "butter to baking at dawn, and one entrant last year was caught "
            "trying to read her recipe card through binoculars. Mrs. "
            "Abernathy, who is eighty-three, accepted the ribbon with her "
            "usual modesty and then announced, to gasps from the tent, that "
            "next year she might try muffins."
        ),
    },
    {
        "title": "The Library Starts Lending Cake Pans",
        "author": "Julia",
        "publication": COURIER,
        "approved": True,
        "days_ago": 6,
        "content": (
            "Tucked between the cookbooks and the gardening magazines, the "
            "Willow Creek Library now has a new collection: forty-two cake "
            "pans, available to borrow for two weeks with any library card. "
            "There are pans shaped like castles, trains, sunflowers, and one, "
            "donated anonymously, shaped like a slightly worried owl. Head "
            "librarian Tom Reyes says the idea came from a patron who needed "
            "a dinosaur pan for exactly one birthday party. The owl has been "
            "checked out every week since the collection opened, and nobody "
            "is quite sure why."
        ),
    },
    {
        "title": "Firehouse Chili Night Raises Record Sum",
        "author": "Julia",
        "publication": COURIER,
        "approved": False,
        "days_ago": 3,
        "content": (
            "The Station 3 firefighters served more than six hundred bowls of "
            "chili on Saturday night, raising a record sum for the new "
            "playground on Maple Street. The secret recipe, guarded more "
            "closely than the fire truck keys, came in three strengths: Mild, "
            "Medium, and Call Us If You Need Us. Volunteers from the high "
            "school band played in the engine bay, and the evening ended with "
            "the traditional ringing of the station bell, which several "
            "children were allowed to pull. The playground is expected to "
            "open in the spring."
        ),
    },
    {
        "title": "Letters from a Lighthouse Keeper's Garden",
        "author": "Julia",
        "publication": None,
        "approved": True,
        "days_ago": 10,
        "content": (
            "On the cliff above Gull Point there is a lighthouse that no "
            "longer needs a keeper, and beside it a garden that has never "
            "stopped being tended. The woman who looks after it, a retired "
            "schoolteacher, plants whatever the seed packets left in the old "
            "keeper's shed tell her to, even when the handwriting is faded "
            "and the instructions are strange. This year that meant a row of "
            "sweet peas, a patch of blue potatoes, and a single sunflower "
            'labeled only "For Eliza." She has no idea who Eliza was. She '
            "plants it anyway, every year, facing the sea."
        ),
    },
    {
        "title": "The Bicycle That Came Home After Forty Years",
        "author": "Julia",
        "publication": None,
        "approved": False,
        "days_ago": 0,
        "content": (
            "In 1985, a red bicycle with a wicker basket was stolen from "
            "outside the post office on Main Street. Last Tuesday it was "
            "leaning against the same wall, freshly painted, its tires pumped "
            "and its basket full of daffodils. A note tucked under the bell "
            'said only "Sorry it took so long." The bicycle\'s original '
            "owner, now a grandmother of five, rode it slowly around the "
            "block while half the street applauded. She says she is not "
            "interested in finding out who took it. She would just like to "
            "know where it has been."
        ),
    },
    {
        "title": "The Bridge Painters Who Only Work at Night",
        "author": "Jonah",
        "publication": GAZETTE,
        "approved": True,
        "days_ago": 6,
        "content": (
            "Every summer, while the city sleeps, a crew of six painters "
            "climbs the Iron Street Bridge and gives it a fresh coat of "
            "green, one rivet at a time. They work from midnight to dawn so "
            "the traffic can keep moving, guided by headlamps and a radio "
            "tuned permanently to the late-night jazz station. Foreman Abe "
            "Lindqvist says the job takes four summers to finish, by which "
            "time the first section needs painting again. He does not mind. "
            "He says the best view of the city is the one you get at four in "
            "the morning, hanging over the river with a brush in your hand."
        ),
    },
    {
        "title": "The Town's Oldest Oak Gets a Birthday Cake",
        "author": "Jonah",
        "publication": COURIER,
        "approved": True,
        "days_ago": 8,
        "content": (
            "Nobody knows exactly how old the great oak on Mill Lane is, but "
            "the town historical society settled on three hundred years and "
            "decided that was reason enough for a party. On Sunday afternoon, "
            "neighbors gathered under its branches with folding chairs, "
            "lemonade, and a sheet cake decorated with three hundred tiny "
            "frosting acorns. The mayor gave a short speech, a choir of "
            "second graders sang, and the cake was cut by the oldest resident "
            "present, a retired farmer of ninety-seven who said he had "
            "climbed the tree as a boy and fully expected it to outlive him."
        ),
    },
    {
        "title": "Saturday Soup Swap Outgrows the Church Hall",
        "author": "Jonah",
        "publication": COURIER,
        "approved": False,
        "days_ago": 1,
        "content": (
            "What began last winter as six neighbors trading jars of homemade "
            "soup has grown so popular that the Saturday Soup Swap needs a "
            "new home. Last week more than eighty people arrived with "
            "containers of minestrone, lentil, chowder, and one memorable pot "
            "of something its maker would only describe as Tuesday. The rules "
            "are simple: bring a jar, take a jar, and write the ingredients "
            "on the lid. Organizers are now talking with the high school "
            "about using its cafeteria, and have quietly asked whoever "
            "brought Tuesday to share the recipe."
        ),
    },
    {
        "title": "Notes from a Rooftop Beekeeper",
        "author": "Jade",
        "publication": None,
        "approved": True,
        "days_ago": 9,
        "content": (
            "Three floors above the laundromat on Fenwick Street, I keep two "
            "hives of bees that have never seen a meadow. They forage instead "
            "on window boxes, park lindens, and the overgrown lot behind the "
            "bakery, and their honey tastes a little different every month, "
            "like a map of whatever is blooming somewhere below. People ask "
            "whether the bees mind the city. As far as I can tell, they treat "
            "it as one enormous, untidy garden, which on most mornings is "
            "exactly what it looks like from up here."
        ),
    },
    {
        "title": "The Umbrella Library at the Number 12 Bus Stop",
        "author": "Jade",
        "publication": None,
        "approved": False,
        "days_ago": 2,
        "content": (
            "Someone has started an umbrella library at the Number 12 bus "
            "stop. A coat rack appeared there two weeks ago, hung with a "
            "dozen mismatched umbrellas and a hand-lettered sign that reads "
            '"Take one when it rains, bring one back when it does not." So '
            "far the system seems to be working. On wet mornings the rack "
            "empties within an hour, and by the next afternoon it is full "
            "again, sometimes with more umbrellas than before. Nobody has "
            "claimed responsibility, but the handwriting on the sign looks a "
            "great deal like the chalkboard outside the florist across the "
            "street."
        ),
    },
]

# The demo newsletters: one for each publication by its own journalist,
# one each of James's and Julia's independent work, and Jonah's Gazette
# Weekend Edition, which includes James's Night Market article, so that
# article is in two newsletters. The author is a username from USERS,
# publication is None for an independent newsletter, and articles are
# titles from ARTICLES. Every article must fit its newsletter: for an
# independent one, the author's own approved independent articles; for
# a publication's, that publication's approved articles, whoever wrote
# them. days_ago sets how long ago the newsletter was created. For
# example:
#     "Lamplight After Dark"  # James's newsletter for the Gazette
NEWSLETTERS = [
    {
        "title": "Lamplight After Dark",
        "days_ago": 5,
        "author": "James",
        "publication": GAZETTE,
        "description": (
            "The best of The Lamplight Gazette, for readers who do their "
            "reading after the sun goes down."
        ),
        "articles": [
            "Night Market Lanterns Return to Canal Street",
            "City Council Votes to Keep the Old Clock Tower Ticking",
        ],
    },
    {
        "title": "Notes from the Night Walk",
        "days_ago": 9,
        "author": "James",
        "publication": None,
        "description": (
            "James's own essays and odd discoveries from the city's "
            "quieter hours."
        ),
        "articles": [
            "What the Fog Remembers",
        ],
    },
    {
        "title": "The Kettle's Weekly Pour",
        "days_ago": 4,
        "author": "Julia",
        "publication": COURIER,
        "description": (
            "A warm roundup of The Copper Kettle Courier's favorite "
            "stories from around town."
        ),
        "articles": [
            "Mrs. Abernathy's Scones Win the County Fair, Again",
            "The Library Starts Lending Cake Pans",
        ],
    },
    {
        "title": "Postcards from Gull Point",
        "days_ago": 7,
        "author": "Julia",
        "publication": None,
        "description": (
            "Julia's independent stories about small places and the "
            "people who look after them."
        ),
        "articles": [
            "Letters from a Lighthouse Keeper's Garden",
        ],
    },
    {
        "title": "Gazette Weekend Edition",
        "days_ago": 3,
        "author": "Jonah",
        "publication": GAZETTE,
        "description": (
            "Jonah's weekend picks from The Lamplight Gazette, by "
            "everyone on its staff."
        ),
        "articles": [
            "The Bridge Painters Who Only Work at Night",
            "Night Market Lanterns Return to Canal Street",
        ],
    },
]
