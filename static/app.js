function App() {
    const boxes = Array.from({ length: 10 }, (_, index) => index + 1);
    
    const boxStyle = {
        border: '2px solid #333',
        borderRadius: '8px',
        padding: '20px',
        margin: '10px',
        backgroundColor: '#f5f5f5',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        width: '200px'
    };

    const containerStyle = {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '20px',
        padding: '20px'
    };

    return (
        <div style={containerStyle}>
            {boxes.map((box) => (
                <div key={box} style={boxStyle}>
                    <h1>Hello World</h1>
                </div>
            ))}
        </div>
    );
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
); 