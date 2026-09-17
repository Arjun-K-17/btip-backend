import { useEffect, useRef, useState } from "react";


function AIChatbot({ companyId }) {
  const [isOpen, setIsOpen] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I'm your BTIP Business Turnaround Assistant. Ask me about your company's financial health, risks, crisis indicators, or recommendations."
    }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;


  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages, loading]);


  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  }, [isOpen]);


  const sendMessage = async () => {
    const question = input.trim();

    if (!question || loading) {
      return;
    }


    if (!companyId) {
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "user",
          content: question
        },
        {
          role: "assistant",
          content:
            "Please select a company before using the BTIP Business Turnaround Assistant."
        }
      ]);

      setInput("");

      return;
    }


    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: question
      }
    ]);

    setInput("");
    setLoading(true);


    try {
      const response = await fetch(
        `${API_BASE_URL}/chatbot/ask`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            company_id: Number(companyId),
            question
          })
        }
      );


      const data = await response.json();


      if (!response.ok) {
        let errorMessage =
          "Unable to get a response from the BTIP AI Assistant.";


        if (typeof data.detail === "string") {
          errorMessage = data.detail;
        } else if (data.detail?.message) {
          errorMessage = data.detail.message;
        }


        throw new Error(errorMessage);
      }


      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content:
            data.answer ||
            "The AI Assistant did not return a response."
        }
      ]);

    } catch (error) {
      console.error(
        "BTIP AI Assistant error:",
        error
      );


      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Unable to connect to the BTIP AI Assistant."
        }
      ]);

    } finally {
      setLoading(false);
    }
  };


  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };


  const clearConversation = () => {
    setMessages([
      {
        role: "assistant",
        content:
          "Conversation cleared. What would you like to know about your company's financial health?"
      }
    ]);
  };


  return (
    <>
      {isOpen && (
        <div className="ai-chatbot-window">

          <div className="ai-chatbot-header">

            <div className="ai-chatbot-header-info">

              <div className="ai-chatbot-avatar">
                💼
              </div>

              <div>
                <strong>
                  BTIP AI Assistant
                </strong>

                <span>
                  Business Turnaround Assistant
                </span>
              </div>

            </div>


            <div className="ai-chatbot-header-actions">

              <button
                type="button"
                className="ai-chatbot-clear"
                onClick={clearConversation}
                title="Clear conversation"
              >
                ↻
              </button>

              <button
                type="button"
                className="ai-chatbot-close"
                onClick={() => setIsOpen(false)}
                title="Close assistant"
              >
                ×
              </button>

            </div>

          </div>


          <div className="ai-chatbot-company">

            <span className="ai-chatbot-company-dot">
              ●
            </span>

            <span>
              {companyId
                ? `Analyzing selected company #${companyId}`
                : "No company selected"}
            </span>

          </div>


          <div className="ai-chatbot-messages">

            {messages.map((message, index) => (
              <div
                key={index}
                className={
                  message.role === "user"
                    ? "ai-chatbot-message user"
                    : "ai-chatbot-message assistant"
                }
              >

                {message.role === "assistant" && (
                  <div className="ai-chatbot-message-avatar">
                    💼
                  </div>
                )}

                <div className="ai-chatbot-message-content">
                  {message.content}
                </div>

              </div>
            ))}


            {loading && (
              <div className="ai-chatbot-message assistant">

                <div className="ai-chatbot-message-avatar">
                  💼
                </div>

                <div className="ai-chatbot-typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

              </div>
            )}


            <div
              ref={messagesEndRef}
            />

          </div>


          <div className="ai-chatbot-suggestions">

            <button
              type="button"
              onClick={() =>
                setInput(
                  "Summarize the financial condition of this company."
                )
              }
              disabled={loading || !companyId}
            >
              Financial summary
            </button>

            <button
              type="button"
              onClick={() =>
                setInput(
                  "What is the biggest financial problem facing this company?"
                )
              }
              disabled={loading || !companyId}
            >
              Biggest problem
            </button>

            <button
              type="button"
              onClick={() =>
                setInput(
                  "What should this company prioritize for turnaround?"
                )
              }
              disabled={loading || !companyId}
            >
              Turnaround priority
            </button>

          </div>


          <div className="ai-chatbot-input-area">

            <textarea
              ref={inputRef}
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder={
                companyId
                  ? "Ask about your company..."
                  : "Select a company first..."
              }
              disabled={
                loading || !companyId
              }
              rows={1}
            />

            <button
              type="button"
              className="ai-chatbot-send"
              onClick={sendMessage}
              disabled={
                loading ||
                !input.trim() ||
                !companyId
              }
              title="Send message"
            >
              ➤
            </button>

          </div>


          <div className="ai-chatbot-footer">
            AI-generated analysis • Verify important decisions
          </div>

        </div>
      )}


      <button
        type="button"
        className={
          isOpen
            ? "ai-chatbot-floating-button open"
            : "ai-chatbot-floating-button"
        }
        onClick={() => setIsOpen(!isOpen)}
        aria-label={
          isOpen
            ? "Close BTIP AI Assistant"
            : "Open BTIP AI Assistant"
        }
        title="BTIP Business Turnaround Assistant"
      >
        {isOpen ? "×" : "💬"}
      </button>

    </>
  );
}


export default AIChatbot;