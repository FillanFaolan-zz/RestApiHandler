# About The Package
This package is designed for use the REST api more easy.

# Requirement
pip install requests

# Useage
## Basic useage
```
    handler = ApiHandler("https://foo.bar/")
    handler = handler.v1.search(key="rest api", limit = 10)
    # This will send a GET request to url https://foo.bar/v1/search?key=rest api&limit=10
    handler.Get()
```

## Dot Parsing

```
    # The "dot" in the path will be replaced by "." if "dot" have both super and sub path.
    handler = ApiHandler("https://foo.bar/")
    search = handler.v1.search.dot.json(key="api")
    # Get-Method url => https://foo.bar/v1/search.json?key=api

    # dot that doesn't have super or sub path will not be converted
    search = handler.v1.search.dot.dot(key="api")
    # Get-Method url => https://foo.bar/v1/search.dot?key=api

    # You can turn off auto-parse by set handler.autoParseDot = False
    search.autoParseDot = False
    # Get-Method url => https://foo.bar/v1/search/dot/dot?key=api
```

## Deal With Api and Function Name Colliding
```
    handler = ApiHandler("https://foo.bar/")
    # AppendPath(str) and AppendPaths(list) allows you to add any kind of path or path serial.
    search = handler.v1.search.AppendPath("Get").dot.json(key="api")
    # Get-Method url => https://foo.bar/v1/search/Get.json?key=api
```

## Send Request
```
    handler = ApiHandler("https://foo.bar/")
    search = handler.v1.search.AppendPath("Get").dot.json(key="api")
    # Parameter can be ResponseType.Json (by default), ResponseType.Xml or ResponseType.Bytes
    jsonGetResponse = search.Get()
    # And .Post() .Head() .Put() .Delete() .Patch() .Options() methods are also available.
```

## When to Give The params
```
    # You can give params anytime while building the url using path(param_name=value).
    handler = ApiHandler("https://foo.bar/")
    # It is equal for following three url build procedure, use anyway you like.
    search = handler.v1.user(id="somebody").group(group_id=1).print(limit=100)
    search = handler.v1.user.group(id="somebody", group_id=1).print(limit=100)
    search = handler.v1.user.group.print(id="somebody", group_id=1, limit=100)
    # Get-Method url => https://foo.bar/v1/user/group/print?key=api&id=somebody&group_id=1&limit=100
```

# License
LGPLv3
