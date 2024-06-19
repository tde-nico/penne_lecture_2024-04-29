window.fetchWrapper = {
    get: request('GET'),
    post: request('POST'),
    put: request('PUT'),
    delete: request('DELETE')
};

function request(method) {
    return (url, body) => {
        /* const requestOptions = { method }
        if (body) {
            requestOptions.headers['Content-Type'] = 'application/json'
            requestOptions.body = JSON.stringify(body)
        }
        return fetch(url, requestOptions).then(handleResponse) */
        const request = new XMLHttpRequest();
        request.open(method, url, false); // `false` makes the request synchronous
        if (body) {
            request.setRequestHeader('Content-Type', 'application/json')
            body = JSON.stringify(body)
        }
        request.send(body)

        return handleResponseSync(request)
    }
}

function handleResponseSync(request) {
    let data = request.responseText
    try {
        data = JSON.parse(data)
    } catch(e) {}
    if (request.status === 200) {
        return data;
    } else {
        const error = (data && data.msg) || request.status
        console.error(`Errore: ${error}`)
        if (request.status == 418){
            alert(error)
        } else if (request.status == 401) {
            setTimeout(function() {
                window.location.reload();
            }, 2000);
            document.querySelector('.quiz-question-text-container').textContent =  "hai già risposto, aspetta la prossima domanda"
        }
        

    }
    return false;
}

// helper functions
async function handleResponse(response) {
    const isJson = response.headers?.get('Content-Type')?.includes('application/json');
    const data = isJson ? await response.json() : null;

    // check for error response
    if (!response.ok) {
        if (response.status == 401) {
            alert("Errore! Non sei autenticato!")
        } else {
            const error = (data && data.message) || response.status
            alert(`Errore: ${error}`)
        }
        return false;
    }
    console.log(data);
    return data;
}