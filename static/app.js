// Box component for each Hello World item
function Box({ number }) {
    const [isLoading, setIsLoading] = React.useState(false);
    
    const boxStyle = {
        border: '1px solid var(--tg-theme-hint-color, #e0e0e0)',
        borderRadius: '8px',
        padding: '15px',
        margin: '10px',
        backgroundColor: 'var(--tg-theme-bg-color, #ffffff)',
        boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
        width: '300px',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        minHeight: '150px'
    };

    const titleContainerStyle = {
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        marginBottom: '10px'
    };

    const titleStyle = {
        fontSize: '18px',
        color: 'var(--tg-theme-link-color, #0066cc)',
        margin: '0',
        fontWeight: 'bold',
        textDecoration: 'none',
        cursor: 'pointer'
    };

    const loadingIndicatorStyle = {
        width: '20px',
        height: '20px',
        border: '2px solid var(--tg-theme-bg-color, #f3f3f3)',
        borderTop: '2px solid var(--tg-theme-link-color, #0066cc)',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
        display: 'inline-block'
    };

    const descriptionStyle = {
        fontSize: '14px',
        color: 'var(--tg-theme-text-color, #666)',
        margin: '0 0 15px 0'
    };

    const tagStyle = {
        display: 'inline-block',
        padding: '4px 12px',
        backgroundColor: 'var(--tg-theme-secondary-bg-color, #e8f4f4)',
        color: 'var(--tg-theme-button-color, #008080)',
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
        borderTop: '1px solid var(--tg-theme-hint-color, #f0f0f0)'
    };

    const timeStyle = {
        color: 'var(--tg-theme-hint-color, #999)',
        fontSize: '12px'
    };

    const handleClick = async (e) => {
        e.preventDefault();
        console.log(`Starting task for box ${number}...`);
        
        setIsLoading(true);
        
        try {
            const response = await fetch(`/api/task/${number}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            if (window.Telegram && window.Telegram.WebApp) {
                window.Telegram.WebApp.showAlert(data.message);
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Task failed:', error);
            if (window.Telegram && window.Telegram.WebApp) {
                window.Telegram.WebApp.showAlert('Operation failed. Please try again.');
            } else {
                alert('Operation failed. Please try again.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={boxStyle}>
            <div style={titleContainerStyle}>
                <a 
                    href="#" 
                    onClick={handleClick}
                    style={titleStyle}
                >
                    Hello World #{number}
                </a>
                {isLoading && (
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
    );
}

// Main App component
function App() {
    React.useEffect(() => {
        // Initialize Telegram Web App
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.ready();
            window.Telegram.WebApp.expand();
        }

        // Add the spinning animation
        const styleSheet = document.createElement("style");
        styleSheet.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(styleSheet);

        return () => {
            document.head.removeChild(styleSheet);
        };
    }, []);

    const containerStyle = {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '20px',
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto'
    };

    return (
        <div style={containerStyle}>
            {Array.from({ length: 10 }, (_, index) => (
                <Box key={index + 1} number={index + 1} />
            ))}
        </div>
    );
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
); 