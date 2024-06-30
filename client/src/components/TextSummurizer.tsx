import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { useState, useEffect, useRef } from "react"
import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
  } from "@/components/ui/resizable"
  
  import {
    Alert,
    AlertDescription,
    AlertTitle,
  } from "@/components/ui/alert"
  
  import {
    Tabs,
    TabsList,
    TabsTrigger,
  } from "@/components/ui/tabs"
import { Loader2 } from "lucide-react"
import axios from "axios"
  


export function TextareaWithButton() {

    const [model, setModel] = useState(0)
    const [text, settext] = useState("");
    // const [summary, setsummary] = useState("Your summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be hereYour summary will be here\nYour summary will be here");
    const [loading, setloading] = useState(false)
    const [summary, setsummary] = useState("Your summary will be here")



    const handleSummit = async () =>{

        setloading(true)
        try {
            const response = await axios.post("http://localhost:8000/textsummarize",
            {"model":model, "text":text}
            )
    
    
            // Check if the request was successful (status code 2xx)
            if (response.status==201) {
            const data = await response.data;
            setsummary(data)
            setloading(false)
            } else {
            // Handle errors or check the response status for more information
            throw new Error(`HTTP error! Status: ${response.status}`);
            // console.log(response,"catched")
    
            }
        } catch (error) {
            // Handle errors that occurred during the fetch
            console.error('Fetch Error:', error);
            setsummary("There is error in summary, Try again Later")
            setloading(false)
        }

    }


  return (
    <div className="h-[550px] mb-24">
        <Alert>
            {/* <RocketIcon className="h-4 w-4" /> */}
            <AlertTitle>Summarize!</AlertTitle>
            <AlertDescription>
            You can summarize your amharic text here.
            </AlertDescription>
      </Alert>


        <ResizablePanelGroup
        direction="horizontal"
        className="h-full w-full rounded-lg border"
      >
        <ResizablePanel defaultSize={50}>
          <div className="flex flex-col h-full p-6 gap-6">   
            <Textarea required onChange={(e)=> settext(e.target.value)} value={text} className="resize-none w-full min-h-[380px]" placeholder="Type your message here." />
            <Tabs defaultValue="extractive" className="w-full">
                <TabsList className="w-full grid grid-cols-3">
                    <TabsTrigger className="h-10" onClick={()=> setModel(0)} value="extractive">Extractive</TabsTrigger>
                    <TabsTrigger className="h-10" onClick={()=> setModel(1)} value="cosine">Cosine-Sim</TabsTrigger>
                    <TabsTrigger title="news Articles" className="h-10" onClick={()=> setModel(2)} value="abstractive">Abstractive</TabsTrigger>

                </TabsList>
            </Tabs>
            <Button onClick={handleSummit} className="w-full self-end">Summarize</Button>
          </div>
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={50}>
   {
    loading ?(
        <div className="flex flex-col h-full p-6 gap-6">

            <div className='relative min-h-full bg-zinc-50 flex divide-y divide-zinc-200 flex-col justify-between gap-2'>
            <div className='flex-1 flex justify-center items-center flex-col mb-28'>
                <div className='flex flex-col items-center gap-2'>
                    <Loader2 className='h-8 w-8 text-blue-500 animate-spin' />
                    <h3 className='font-semibold text-xl'>
                     በማጠቃለል ላይ...
                    </h3>
                    <p className='text-zinc-500 text-sm'>
                    </p>
                </div>
                 </div>
            </div>
            </div>
     
    ):
    <div className="flex flex-col h-full p-6 gap-6">

        <Textarea value={summary} className="resize-none w-full min-h-[500px]" placeholder="Type your message here." />

    </div>

   }
        </ResizablePanel>
      </ResizablePanelGroup>
    



    </div>

  )
}




