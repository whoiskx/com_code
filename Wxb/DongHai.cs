using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Spider;
using Http;

namespace Script
{
    class DongHai : Processor
    {
        public override void GetSource(TaskState taskState, ProcState procState)
        {
            string url = procState.urlData.uri.AbsoluteUri;
            if (procState.urlData.layer == 0)
            {
                base.GetSource(taskState, procState);
            }
            else
            {
                string sou = Downloader.Download(url);
                string nurl = RegexUtil.MatchText(sou, "http.*aspx");
                string source = Downloader.Download(nurl);
                if (!string.IsNullOrEmpty(source))
                {
                    procState.pageData.source = source;
                }

                Html.HtmlDocument htmlDoc = new Html.HtmlDocument();
                htmlDoc.LoadHtml(procState.pageData.source);
                procState.pageData.htmlDoc = htmlDoc;
            }
        }
    }
}
