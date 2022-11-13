import copy
import re

class Nom:
  pass

noms = []
spreadsheetConstant = 30
isSupportSection = False
isOpposeSection = False

patternArticle = "^\[\[Wookieepedia:Comprehensive article nominations/.*\]\]$"
patternResult = (
  "^:''The following discussion is preserved as an archive " +
  "of a \[\[Wookieepedia:Comprehensive article nominations\|Comprehensive " +
  "article nomination\]\] that was '''.*'''."
)
patternNominator = "^\*'''Nominated by''':.*$"
patternWPs = "^\*'''WookieeProject \(optional\)''':.*$"
patternVotes = "^====Support====.*$"
patternComments = "^====Comments====.*$"
patternObjectors = "^====Object====.*$"
patternEnddate = "^\{\{.*approved\|.*$"
WPlist = [["Wookieepedia:WookieeProject Aliens", "WP:ALIENS", "WP:AS"],
["Wookieepedia:WookieeProject Ambition", "WP:AMB"],
["Wookieepedia:WookieeProject Astrography", "WP:AST"],
["Wookieepedia:WookieeProject Battlefront", "WP:Battlefront", "WP:BF", "WP:SWBF"],
["Wookieepedia:WookieeProject Chiss", "WP:Chiss", "WP:CHISS"],
["Wookieepedia:WookieeProject Comics", "WP:CO", "WP:COMICS"],
["Wookieepedia:WookieeProject Creators", "WP:CREA", "WP:CREATORS"],
["Wookieepedia:WookieeProject Data Seekers", "WP:DS"],
["Wookieepedia:WookieeProject Durge's Lance", "WP:CIS", "WP:SEP"],
["Wookieepedia:WookieeProject Entertainment and Culture",
"WP:ENT",
"WP:EAC",
"Wookieepedia:WookieeProject Entertainment",
"WP:Entertainment"],
["Wookieepedia:WookieeProject Ewoks", "WP:E", "WP:Ewoks", "WP:EWOKS"],
["Wookieepedia:WookieeProject Fantasy Flight Games", "WP:FFGAMES", "WP:FFG"],
["Wookieepedia:WookieeProject Galaxies", "WP:SWG"],
["Wookieepedia:WookieeProject Galaxy's Edge", "WP:GE"],
["Wookieepedia:WookieeProject Knights of the Old Republic", "WP:KOTOR"],
["Wookieepedia:WookieeProject Legacy's Era", "WP:Legacy", "WP:LE"],
["Wookieepedia:WookieeProject LEGO", "WP:LEGO"],
["Wookieepedia:WookieeProject New Sith Wars", "WP:NSW"],
["Wookieepedia:WookieeProject Novels",
"WP:N",
"WP:Novels",
"Wookieeproject: Novels",
"WP:NOVELS"],
["Wookieepedia:WookieeProject Pride", "WP:PRIDE", "WP:Pride"],
["Wookieepedia:WookieeProject Rebels", "WP:Rebels", "WP:REBELS", "WP:SWR"],
["Wookieepedia:WookieeProject Resistance", "WP:Resistance", "WookieeProject: Resistance"],
["Wookieepedia:WookieeProject Star Wars: Card Trader", "WP:SWCT"],
["Wookieepedia:WookieeProject Tales of the Jedi", "WP:TOTJ", "WP:Totj"],
["Wookieepedia:WookieeProject The Clone Wars", "WP:TCW", "WookieeProject The Clone Wars"],
["Wookieepedia:WookieeProject The High Republic", "WP:THR"],
["Wookieepedia:WookieeProject The Mandalorian", "WP:Mando", "WP:TMND"],
["Wookieepedia:WookieeProject The New Jedi Order", "WP:NJO"],
["Wookieepedia:WookieeProject The Old Republic", "WP:TOR"],
["Wookieepedia:WookieeProject Video Games", "WP:VG"],
["Wookieepedia:WookieeProject Warfare", "WP:Warfare"],
["Wookieepedia:WookieeProject Women", "WP:WOMEN", "WP:Women"]
]

f = open("ca_nom_archive_2022.txt", "r")
for x in f:

  # process nom article title

  if re.search(patternArticle, x):
    currentNom = Nom()
    currentNom.WPs = []
    currentNom.objectors = []
    currentNom.article = re.sub(
      "(^\[\[Wookieepedia:Comprehensive article nominations/|\]\])",
      "",
      x
    ).strip()


  # process nom result

  elif re.search(patternResult, x):
    currentNom.result = re.sub(
      (
        "(^:''The following discussion is preserved as an archive of a " +
        "\[\[Wookieepedia:Comprehensive article nominations\|Comprehensive " +
        "article nomination\]\] that was '''|\.|''')"
      ),
      "",
      x
    ).strip()


  # process nominator name and nom start date

  elif re.search(patternNominator, x):
    # process nominator
    string = re.sub("^\*'''Nominated by''':[^\[]*", "", x).strip()
    #namePart = re.findall("\[\[User:.*\|", string)[0] # ignores co-nominators!
    namePart = "[[User:Manoof|"
    name = re.sub("(\[\[User:|\|.*)", "", namePart)
    currentNom.nominator = name

    # process start date
    # datePart = re.findall(
    #   (
    #     "\d\d:\d\d# \d+ (?:January|February|March|April|May|June|" +
    #     "July|August|September|October|November|December) \d\d\d\d \(UTC\)"
    #   ),
    #   string
    # )[0]
    datePart = "14:19# 24 June 2020"

    date = re.sub(" \(UTC\)", "", datePart)
    currentNom.startdate = date


  # process WPs

  elif re.search(patternWPs, x):
    currentNom.WPs = []
    
    # trim field text, strip spaces, convert to uppercase
    WPfield = re.sub(
      "^\*'''WookieeProject \(optional\)''':",
      "",
      x
    ).strip().upper()

    # fetch and save WPs
    for WookieeProject in WPlist:
      for WPname in WookieeProject:
        if re.search(WPname.upper(), WPfield):
          currentNom.WPs.append(
            re.sub("Wookieepedia:WookieeProject ", "", WookieeProject[0])
          )


  # process support votes

  # initialize
  elif re.search(patternVotes, x):
    isSupportSection = True
    currentNom.votes = []

  # process each vote
  elif re.search("^#", x):
    if isSupportSection:
      # omit struck votes
      if re.search("^#:<s>", x):
        pass

      # fetch and save review panel vote tag if present
      else:
        if re.search("^#(\{\{Inq\}\}|\{\{AC\}\}|\{\{EC\}\})", x):
          currentNom.votes.append(
            re.findall("^#(\{\{Inq\}\}|\{\{AC\}\}|\{\{EC\}\})", x)[0]
          )
        else:
          currentNom.votes.append("")
        
        # fetch and save username from vote
        #namePart = re.findall("\[\[User:.*\|", x)[0]
        namePart = "[[User:Manoof|"
        name = re.sub("(\[\[User:|\|.*)", "", namePart)
        currentNom.votes.append(name)

  # wrap up with support votes
  elif re.search(patternObjectors, x):
    isSupportSection = False
    isOpposeSection = True

    # pad the list with empty entries
    while 2 * spreadsheetConstant > len(currentNom.votes):
        currentNom.votes.append("")

    currentNom.objectors = []
    #PROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEMPROBLEM
    #print(currentNom.objectors)


  # process usernames in objections

  elif re.search("\[\[User:", x):
    if isOpposeSection:
      namePart = re.findall("\[\[User:.*\|", x)[0]
      name = re.sub("(\[\[User:|\|.*)", "", namePart)
      currentNom.objectors.append(name)


  # wrap up with usernames in objections and process nom end date

  elif re.search(patternEnddate, x):
    isOpposeSection = False

    # remove duplicate usernames and
    # sort the list of usernames mentioned in objections alphabetically
    currentNom.objectors = list(dict.fromkeys(currentNom.objectors))
    currentNom.objectors.sort()

    # remove nominator from the above list
    if currentNom.nominator in currentNom.objectors:
      currentNom.objectors.remove(currentNom.nominator)

    # remove support voter names from the list
    for y in currentNom.votes:
      if y in currentNom.objectors:
        currentNom.objectors.remove(y)

    # pad the list with empty entries
    while spreadsheetConstant > len(currentNom.objectors):
        currentNom.objectors.append("")

    # fetch and save the nom end date
    currentNom.enddate = re.sub("(^.*approved\|| \(UTC\)|\}\})", "", x).strip()

    # save the data about the current nom
    noms.append(copy.deepcopy(currentNom))
f.close()


# output the nomination data as a txt (csv) file

separator = "# "
f = open("result.txt", "a")

for x in noms:
    f.write(
      x.article + separator +
      x.result + separator +
      x.nominator + separator +
      x.startdate + separator +
      "; ".join(x.WPs) + separator +
      "# ".join(x.votes) + separator +
      "# ".join(x.objectors) + separator +
      x.enddate + "\n"
    )

f.close()