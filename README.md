# Backend

Backend for FACEIT project

## Request Analysis image

### Request

`POST /create-image`

```code
    Parameters:
        room (string) : room token
    Body: JSON
        img (list of string): each element only need to include the file name, no path needed

```

### Respond

`JSON`

```code
    status (string):
        'OK': everything is OK
        'Error' : There are something wrong, Check errmsg for more info
    errmsg (string): detail error msg

    Following field only appear if status is OK

    room (string): room token
    img (list of string): each element contain the output file name


```
