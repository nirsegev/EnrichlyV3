function App() {
    const boxes = Array.from({ length: 10 }, (_, index) => index + 1);
    
    const boxStyle = {
        border: '2px solid #333',
        borderRadius: '8px',
        padding: '20px',
        margin: '10px',
        backgroundColor: '#f5f5f5',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        width: '200px',
        position: 'relative'
    };

    const containerStyle = {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '20px',
        padding: '20px'
    };

    const textStyle = {
        textAlign: 'center',
        margin: '0'
    };

    const deleteButtonStyle = {
        position: 'absolute',
        bottom: '10px',
        right: '10px',
        background: 'none',
        border: 'none',
        cursor: 'pointer',
        fontSize: '20px',
        color: '#ff4444'
    };

    return (
        <div style={containerStyle}>
            {boxes.map((box) => (
                <div key={box} style={boxStyle}>
                    <h1 style={textStyle}>Hello World</h1>
                    <button style={deleteButtonStyle}>
                        ×
                    </button>
                </div>
            ))}
        </div>
    );
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
); 