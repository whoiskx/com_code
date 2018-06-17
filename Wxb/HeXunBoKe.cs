using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;

using Script.Mobile;
using Spider;
using Common;
using Http;
using Html;
using System.Threading;

namespace Script
{
    class HeXunBoKe : Processor
    {
        public override void GetSource(TaskState taskState, ProcState procState)
        {
            string url = procState.pageData.uri.AbsoluteUri;
            string source = DownGet(taskState, procState, url);
            if (!string.IsNullOrEmpty(source))
            {
                procState.pageData.source = source;
            }
            Html.HtmlDocument htmldoc = new HtmlDocument();
            htmldoc.LoadHtml(procState.pageData.source);
            procState.pageData.htmlDoc = htmldoc;
        }
        public static string DownGet(TaskState taskState, ProcState procState, string url)
        {
            string text = "";
            HttpWebRequest request = null;
            HttpWebResponse response = null;
            Stream myStream = null;
            StreamReader myStreamReader = null;
            try
            {
                request = HttpWebRequest.Create(url) as HttpWebRequest;
                request.Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8";
                request.UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36";
                request.KeepAlive = true;
                request.Headers.Add("Accept-Encoding", "gzip, deflate");
                request.Headers.Add("Accept-Language", "zh-CN,zh;q=0.8");
                request.Method = "Get";
                request.Headers["Cookie"] = "UM_distinctid=1601f9715d61ca-0809906a86f85e-1b1d7551-100200-1601f9715d750; hxck_sq_blog_popbox=1; HEXUN_COM_MEDIA_PLAYSTATE=1; ASP.NET_SessionId=tiwcsp3fla3czakcn5wxaf2u; HexunTrack=SID=20171204113606074b04acc45181c43bda8ca0fd6e2e545ac&CITY=44&TOWN=440100; bdshare_firstime=1512360402749";
                request.AutomaticDecompression = DecompressionMethods.Deflate | DecompressionMethods.GZip;
                try
                {
                    response = request.GetResponse() as HttpWebResponse;
                }
                catch (WebException ex)
                {
                    response = (HttpWebResponse)ex.Response;
                }
                myStream = response.GetResponseStream();
                myStreamReader = new StreamReader(myStream, Encoding.Default);
                text = myStreamReader.ReadToEnd();
                //string content = XpathUtil.GetTexts(hn.DocumentNode, "//div[@class='Custom_UnionStyle']/p", false, "");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }
            finally
            {
                if (response != null)
                {
                    response.Close();
                }
                if (myStream != null)
                {
                    response.Close();
                }
                if (myStreamReader != null)
                {
                    response.Close();
                }
            }
            return text;
        }
    }
}
