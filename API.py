# Aliases

def OK(data, headers=None):
    return _200(data, headers)

def Error(message, headers=None):
    return _400(message, headers)

def NotFound(message, headers=None):
    return _404(message, headers)

def Unauthenticated(message, headers=None):
    return _401(message, headers)

def Created(data, headers=None):
    return _201(data, headers)

# Success

def _200(data, headers=None):
    return success(data, 200, headers)

def _201(data, headers=None):
    return success(data, 201, headers)

# Errors
def _400(message, headers=None):
    return fail({ "message": message }, 400, headers)

def _401(message, headers=None):
    return fail({ "message": message }, 401, headers)

def _404(message, headers=None):
    return fail({ "message": message }, 404, headers)


# Base functionality 
def success(data, code, headers=None):
    return response({ "data": data, "error": { "message": "" }, "success": True }, code, headers)

def fail(data, code, headers=None):
    return response({ "data": None, "error": data, "success": False }, code, headers)


def response(data, code, headers=None):
    respHeaders = { 'Content-Type': 'application/json' }

    if headers:
        for key in headers:
            respHeaders[key] = headers[key]

    return data, code, respHeaders