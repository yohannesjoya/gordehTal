"use client";

import { trpc } from "@/app/_trpc/client";
import ChatInput from "./ChatInput";
import Messages from "./Messages";
import { ChevronLeft, Loader2, XCircle } from "lucide-react";
import Link from "next/link";
import { Button, buttonVariants } from "../ui/button";
import { ChatContextProvider } from "./ChatContext";
import { PLANS } from "@/config/stripe";
import { useState } from "react";
import axios from "axios";
import { Tabs, TabsList, TabsTrigger } from "../ui/tabs";

interface ChatWrapperProps {
  fileId: string;
  fileUrl: string;
  isSubscribed: boolean;
}

const ChatWrapper = ({ fileId, isSubscribed, fileUrl }: ChatWrapperProps) => {
  const [summary, setSummary] = useState<string>("Your Summary will be Here!!");
  const [error, setError] = useState<string>("");
  const [model, setModel] = useState(0);

  const [load, setload] = useState(false);
  const { data, isLoading } = trpc.getFileUploadStatus.useQuery(
    {
      fileId,
    },
    {
      refetchInterval: (data) =>
        // @ts-ignore
        data?.status === "SUCCESS" || data?.status === "FAILED" ? false : 500,
    }
  );

  const handleSummary = async () => {
    setload(true);
    try {
      const response = await axios.post("http://localhost:8000/pdfsummary", {
        url: fileUrl,
        model: model,
      });

      // Check if the request was successful (status code 2xx)
      if (response.status == 201) {
        const data = await response.data;
        setSummary(data);
        setload(false);
      } else {
        // Handle errors or check the response status for more information
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      // Handle errors that occurred during the fetch
      console.error("Fetch Error:", error);
      setError("There is error in summary, Try again Later");
      setload(false);
    }
  };

  if (isLoading || load)
    return (
      <div className="relative min-h-full bg-zinc-50 flex divide-y divide-zinc-200 flex-col justify-between gap-2">
        <div className="flex-1 flex justify-center items-center flex-col mb-28">
          <div className="flex flex-col items-center gap-2">
            <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
            <h3 className="font-semibold text-xl">Loading ላይ...</h3>
            <p className="text-zinc-500 text-sm"></p>
          </div>
        </div>
        <Button className="w-full h-12" disabled>
          Summary
        </Button>
      </div>
    );
  // @ts-ignore
  if (data?.status === "PROCESSING")
    return (
      <div className="relative min-h-full bg-zinc-50 flex divide-y divide-zinc-200 flex-col justify-between gap-2">
        <div className="flex-1 flex justify-center items-center flex-col mb-28">
          <div className="flex flex-col items-center gap-2">
            <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
            <h3 className="font-semibold text-xl">Processing PDF...</h3>
            <p className="text-zinc-500 text-sm">This won&apos;t take long.</p>
          </div>
        </div>
        <Button className="w-full h-12" disabled>
          Summary
        </Button>
      </div>
    );
  // @ts-ignore
  if (data?.status === "FAILED")
    return (
      <div className="relative min-h-full bg-zinc-50 flex divide-y divide-zinc-200 flex-col justify-between gap-2">
        <div className="flex-1 flex justify-center items-center flex-col mb-28">
          <div className="flex flex-col items-center gap-2">
            <XCircle className="h-8 w-8 text-red-500" />
            <h3 className="font-semibold text-xl">Too many pages in PDF</h3>
            <p className="text-zinc-500 text-sm">
              Your{" "}
              <span className="font-medium">
                {isSubscribed ? "Pro" : "Free"}
              </span>{" "}
              plan supports up to{" "}
              {isSubscribed
                ? PLANS.find((p) => p.name === "Pro")?.pagesPerPdf
                : PLANS.find((p) => p.name === "Free")?.pagesPerPdf}{" "}
              pages per PDF.
            </p>
            <Link
              href="/dashboard"
              className={buttonVariants({
                variant: "secondary",
                className: "mt-4",
              })}
            >
              <ChevronLeft className="h-3 w-3 mr-1.5" />
              Back
            </Link>
          </div>
        </div>

        <Button className="w-full h-12" disabled>
          Summary
        </Button>
      </div>
    );

  return (
    <div className="relative h-full bg-zinc-50 flex divide-y divide-zinc-200 flex-col justify-between gap-2">
      <Messages summary={summary} />

      <Tabs defaultValue="extractive" className="w-full">
        <TabsList className="w-full grid grid-cols-2">
          <TabsTrigger
            className="h-10"
            onClick={() => setModel(0)}
            value="extractive"
          >
            Extractive
          </TabsTrigger>
          <TabsTrigger
            className="h-10"
            onClick={() => setModel(1)}
            value="cosine"
          >
            Cosine-Sim
          </TabsTrigger>
          {/* <TabsTrigger className='h-10' onClick={()=> setModel(2)} value="abstractive">Abstractive</TabsTrigger> */}
        </TabsList>
      </Tabs>

      <Button className="w-full h-12" onClick={handleSummary}>
        Summary
      </Button>
    </div>
  );
};

export default ChatWrapper;
