import jsonpickle

SUCCESSFUL_PATCH = jsonpickle.encode({'message:': 'Successful Patch.'}), 200, {
    'Content-Type': 'application/json'
}

UNSUCCESSFUL_PATCH = jsonpickle.encode({'message':
                                        'Unsuccessful Patch.'}), 420, {
                                            'Content-Type': 'application/json'
                                        }
