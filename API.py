def OK(data):
    return _200(data)

def Error(message):
    return _400(message)

def NotFound(message):
    return _404(message)

def Created(data):
    return _201(data)

def _200(data):
    return success(data, 200)

def _201(data):
    return success(data, 201)

def _400(message):
    return fail({ "message": message }, 400)

def _404(message):
    return fail({ "message": message }, 404)

def success(data, code):
    return response({ "data": data, "error": None, "success": True }, code)

def fail(data, code):
    return response({ "data": None, "error": data, "success": False }, code)


def response(data, code):
    return data, code, { 'Content-Type': 'application/json' }