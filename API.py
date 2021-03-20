# Aliases

def OK(data, headers=None):
    return _200(data, headers)

def Created(data, headers=None):
    return _201(data, headers)

def InputError(message, headers=None, title="Input error"):
    return _400(message, headers, title)

def NotFound(message, headers=None, title="Not found"):
    return _404(message, headers, title)

def Unauthorized(message, headers=None, title="Unauthorized"):
    return _401(message, headers, title)


def ServerError(message, headers=None, title="Server error"):
    return _500(message, headers, title)

# Success

def _200(data, headers):
    return success(data, 200, headers)

def _201(data, headers):
    return success(data, 201, headers)

# Errors
def _400(message, headers, title):
    return fail({ "detail": message, "title": title }, 400, headers)

def _401(message, headers, title):
    return fail({ "detail": message, "title": title }, 401, headers)

def _404(message, headers, title):
    return fail({ "detail": message, "title": title }, 404, headers)

def _500(message, headers, title):
    return fail({ "detail": message, "title": title }, 500, headers)

# Base functionality 
def success(data, code, headers):
    return response({ "data": data, "status": code }, code, headers)

def fail(data, code, headers):
    data["status"] = code
    return response(data, code, headers)


def response(data, code, headers):
    respHeaders = { 
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
    }

    if headers:
        for key in headers:
            respHeaders[key] = headers[key]

    return data, code, respHeaders