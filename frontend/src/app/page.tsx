"use client";

import { useState } from "react";
import axios from "axios";
import Image from "next/image";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function Home() {
    const [email, setEmail] = useState<string>("");
    const [topic, setTopic] = useState<string>("");
    const [time, setTime] = useState<string>("08:00:00");

    const handleSubmit = async (e: React.FormEvent) => {
        try {
            e.preventDefault();
            await axios.post("http://localhost:8000/", { email, topic, time });
            alert("Subscribed successfully!");
        } catch (error) {
            alert("An error occurred. Please try again.");
        }
    };

    return (
        <section className="w-full py-12 md:py-24 lg:py-32">
            <div className="container grid max-w-5xl items-center justify-center gap-4 px-4 text-center md:gap-8 md:px-6 lg:grid-cols-2 lg:text-left xl:max-w-6xl xl:gap-10">
                <div className="flex flex-col justify-center space-y-4">
                    <div className="space-y-2">
                        <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl">Loop</h1>
                        <p className="max-w-[500px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                            Stay in the loop with the latest news and updates on the topics you care about.
                        </p>
                    </div>
                    <div className="w-full max-w-sm space-y-2">
                        <form className="flex flex-col gap-2" onSubmit={handleSubmit}>
                            <Input
                                type="email"
                                placeholder="Enter your email"
                                className="max-w-lg"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                            <Input
                                type="text"
                                placeholder="Enter a topic you're interested in"
                                className="max-w-lg"
                                value={topic}
                                onChange={(e) => setTopic(e.target.value)}
                                required
                            />
                            <Select value={time} onValueChange={(value) => setTime(value)} required>
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="08:00:00">Morning - 8:00 am</SelectItem>
                                    <SelectItem value="12:00:00">Noon - 12:00 pm</SelectItem>
                                    <SelectItem value="16:00:00">Afternoon - 4:00 pm</SelectItem>
                                    <SelectItem value="20:00:00">Evening - 8:00 pm</SelectItem>
                                </SelectContent>
                            </Select>
                            <Button type="submit">Subscribe</Button>
                        </form>
                    </div>
                </div>
                <Image
                    src="/news.png"
                    width={500}
                    height={500}
                    style={{ width: "100%", height: "auto" }}
                    alt="Hero"
                    priority
                />
            </div>
        </section>
    );
}
