function App() {
    const [loadingStates, setLoadingStates] = React.useState({});
    const boxes = Array.from({ length: 10 }, (_, index) => index + 1);
    
    const boxStyle = {
        border: '1px solid #e0e0e0',
        borderRadius: '8px',
        padding: '15px',
        margin: '10px',
        backgroundColor: '#ffffff',
        boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
        width: '300px',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        minHeight: '150px'
    };

    const containerStyle = {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '20px',
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto'
    };

    const titleContainerStyle = {
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        marginBottom: '10px'
    };

    const titleStyle = {
        fontSize: '18px',
        color: '#0066cc',
        margin: '0',
        fontWeight: 'bold',
        textDecoration: 'none',
        cursor: 'pointer'
    };

    const loadingIndicatorStyle = {
        width: '20px',
        height: '20px',
        border: '2px solid #f3f3f3',
        borderTop: '2px solid #0066cc',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
        display: 'inline-block'
    };

    // Add the spinning animation
    const styleSheet = document.createElement("style");
    styleSheet.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(styleSheet);

    const descriptionStyle = {
        fontSize: '14px',
        color: '#666',
        margin: '0 0 15px 0'
    };

    const tagStyle = {
        display: 'inline-block',
        padding: '4px 12px',
        backgroundColor: '#e8f4f4',
        color: '#008080',
        borderRadius: '15px',
        fontSize: '12px',
        marginRight: '8px'
    };

    const footerStyle = {
        marginTop: 'auto',
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'center',
        paddingTop: '10px',
        borderTop: '1px solid #f0f0f0'
    };

    const timeStyle = {
        color: '#999',
        fontSize: '12px'
    };

    const handleClick = async (boxNumber) => {
        console.log(`Starting task for box ${boxNumber}...`);
        
        // Set loading state for this box
        setLoadingStates(prev => ({ ...prev, [boxNumber]: true }));
        
        try {
            const response = await fetch(`/api/task/${boxNumber}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            alert(data.message);
        } catch (error) {
            console.error('Task failed:', error);
            alert('Operation failed. Please try again.');
        } finally {
            // Clear loading state
            setLoadingStates(prev => ({ ...prev, [boxNumber]: false }));
        }
    };

    return (
        <div style={containerStyle}>
            {boxes.map((box) => (
                <div key={box} style={boxStyle}>
                    <div style={titleContainerStyle}>
                        <a 
                            href="#" 
                            onClick={(e) => {
                                e.preventDefault();
                                handleClick(box);
                            }} 
                            style={titleStyle}
                        >
                            Hello World #{box}
                        </a>
                        {loadingStates[box] && (
                            <div style={loadingIndicatorStyle} />
                        )}
                    </div>
                    <p style={descriptionStyle}>
                        A sample description text that gives more context about this Hello World item.
                    </p>
                    <div>
                        <span style={tagStyle}>AI</span>
                        <span style={tagStyle}>Mindfulness</span>
                    </div>
                    <div style={footerStyle}>
                        <span style={timeStyle}>2 days ago</span>
                    </div>
                </div>
            ))}
        </div>
    );
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
); 