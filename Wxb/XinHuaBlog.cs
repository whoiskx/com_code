using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Spider;
using Html;
using Common;
using Topic;
using Http;
using System.Text.RegularExpressions;
using Text;

namespace Script
{
    class XinHuaBlog : Processor
    {
        public override void GetSource(TaskState taskState, ProcState procState)
        {
            string url = procState.urlData.uri.AbsoluteUri;
            string source = Downloader.Download(url);
            if (procState.urlData.layer == 0)
            {
                string strurl = RegexUtil.MatchText(url, "http://.*?/blog");
                string param = RegexUtil.MatchText(source, "latestArticleList.*?bid=\\d+");
                if (!string.IsNullOrEmpty(source))
                {
                    source = Http.Downloader.Download(strurl + "/" + param);
                }
            }
            if (!string.IsNullOrEmpty(source))
            {
                procState.pageData.source = source;
            }
            Html.HtmlDocument htmlDoc = new Html.HtmlDocument();
            htmlDoc.LoadHtml(procState.pageData.source);
            procState.pageData.htmlDoc = htmlDoc;
        }
        public override void ParseUrl(TaskState taskState, ProcState procState)
        {
            Task task = taskState.task;
            UrlData urlData = procState.urlData;
            UrlCache urlCache = taskState.urlCache;

            int layer = urlData.layer + 1;
            string source = procState.pageData.source.Replace("\\", "");

            List<string> urls = RegexUtil.MatchTextCollection(source, "(?<url>http://.*?.home.news.cn/blog/a/.*?.html)", "url");
            StringUtil.FilterRepeat(urls);
            foreach (string url in urls)
            {
                Uri uri = new Uri(url);
                UrlType urlType = UrlMatcher.Match(url, layer, task);

                UrlData newUrlData = new UrlData(uri, "", layer, UrlType.Text);
                taskState.logDatas.matched++;
                urlCache.Enqueue(taskState.logDatas, newUrlData);
            }
            taskState.logDatas.totalCount = urls.Count;
        }

        public override void ParseText(TaskState taskState, ProcState procState)
        {
            TextEntity textEntity = procState.pageData.textEntity;
            HtmlNode hn = procState.pageData.htmlDoc.DocumentNode;
            textEntity.title = XpathUtil.GetText(hn, "//div[@id='doc_content']/h1/span/text()");
            textEntity.content = XpathUtil.GetTexts(hn, "//p", false, " ");
            string time = XpathUtil.GetText(hn, "//td[@width='30%']");
            textEntity.time = Time.TimeParser.Parse(time)[0];
            textEntity.author = XpathUtil.GetText(hn, "//span/a[@class='lemu12l']").Replace("&nbsp;","");
        }
    }
}
