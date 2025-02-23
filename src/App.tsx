import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Moon, Sun, Send } from "lucide-react";
import { useTheme } from "@/hooks/use-theme";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
  isErrorMessage?: boolean;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { theme, toggleTheme } = useTheme();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async () => {
    if (!description.trim() || !price.trim()) return;

    const userMessage = `${description.trim()} $${parseFloat(price).toFixed(
      2
    )}`;

    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        content: userMessage,
        role: "user",
        timestamp: new Date(),
      },
    ]);

    setIsLoading(true);
    setDescription("");
    setPrice("");

    // Simulate AI response
    setTimeout(async () => {
      fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description: description,
          price: price,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          // console.log("Image URL:", data.image_url);

          setMessages((prev) => [
            ...prev,
            {
              id: crypto.randomUUID(),
              content: data.image_url,
              role: "assistant",
              timestamp: new Date(),
            },
          ]);
        })
        .catch((err) => {
          setMessages((prev) => [
            ...prev,
            {
              id: crypto.randomUUID(),
              content:
                "Erreur lors de la génération de l'image (" +
                err?.message +
                ")",
              role: "assistant",
              timestamp: new Date(),
              isErrorMessage: true,
            },
          ]);
        });
      setIsLoading(false);
    }, 1500);
  };

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  return (
    <div className={`min-h-screen ${theme}`}>
      <div className="max-w-[800px] mx-auto h-screen flex flex-col">
        {/* Header */}
        <header className="p-4 border-b flex justify-between items-center bg-background">
          <h1 className="text-xl font-semibold">CarGen Inc.</h1>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === "dark" ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
          </Button>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-5">
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex flex-col max-w-[80%] animate-in fade-in duration-300",

                message.role === "user"
                  ? "ml-auto items-end"
                  : "mr-auto items-start"
              )}
            >
              <div
                className={cn(
                  "rounded-lg px-4 py-2",
                  message.role === "user"
                    ? "bg-[#2A7FDB] text-white"
                    : "bg-muted",
                  message.isErrorMessage ? "bg-red-700 text-white" : ""
                )}
              >
                {message.isErrorMessage || message.role === "user" ? (
                  message.content
                ) : (
                  <img
                    src={message.content}
                    className="w-[650px] h-[450px] object-cover"
                  />
                )}
              </div>
              <span className="text-xs text-muted-foreground mt-1">
                {formatTime(message.timestamp)}
              </span>
            </div>
          ))}
          {isLoading && (
            <div className="flex items-center space-x-2 max-w-[80%]">
              <div className="flex space-x-1">
                <span
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                  style={{ animationDelay: "0s" }}
                ></span>
                <span
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                ></span>
                <span
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                  style={{ animationDelay: "0.4s" }}
                ></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Section */}
        <div className="border-t bg-background p-4">
          <div className="max-w-[800px] mx-auto space-y-4">
            <Textarea
              placeholder="Enter your description..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="min-h-[100px] resize-none"
              maxLength={1000}
            />
            <div className="flex gap-4">
              <div className="relative flex-1">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                  $
                </span>
                <Input
                  type="number"
                  placeholder="0.00"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  className="pl-7"
                  step="0.01"
                  min="0"
                />
              </div>
              <Button
                onClick={handleSubmit}
                disabled={!description.trim() || !price.trim() || isLoading}
                className="w-24"
              >
                {isLoading ? (
                  <div className="w-5 h-5 border-2 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </Button>
            </div>
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>{description.length}/1000 characters</span>
              {price && !isNaN(parseFloat(price)) && (
                <span>Price: ${parseFloat(price).toFixed(2)}</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
