def success_response(message: str, data=None):
    return{
        "status": True,
        "message": message,
        "data": data
    }
