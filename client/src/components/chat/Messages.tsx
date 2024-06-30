import { useState, useEffect } from "react"
import Skeleton from 'react-loading-skeleton'
import "axios"
import axios from "axios"
import { Card } from "../ui/card"
import { Button } from "../ui/button"
import { Textarea } from "../ui/textarea"

interface MessagesProps {
  summary:string
}

const Messages = ({ summary }: MessagesProps) => {

 

  return (

    <Textarea value={summary} className="resize-none w-full min-h-[80%]" placeholder="Type your message here." />
      
  )
}

export default Messages

















