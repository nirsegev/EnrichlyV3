import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';

const App = () => {
    const [data, setData] = useState({ greeting: 'fffffffff', message: 'dddddddddd' });

    useEffect(() => {
        fetch('/')
            .then(response => response.json())
            .then(data => setData(data));
    }, []);

    return (
        <div>
            <h1>{data.greeting}</h1>
            <p>{data.message}</p>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));
