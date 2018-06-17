using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Spider;
using Text;
using Html;
using Topic;

namespace Script
{
    class Jqka : Processor
    {
        public override void ParseText(TaskState taskState, ProcState procState)
        {
            try
            {
                string title = "";
                string time = "";
                string author = "";
                string content = "";

                TextEntity textEntity = procState.pageData.textEntity;
                HtmlNode hn = procState.pageData.htmlDoc.DocumentNode;
                string source = procState.pageData.source;

                foreach (KeyValuePair<string, Pattern> kvp in taskState.template)
                {
                    switch (kvp.Key)
                    {
                        case "title":
                             string titles = XpathUtil.GetText(hn, kvp.Value.text);
                            title = RegexUtil.MatchText(titles, @".*?-");
                            break;
                        case "time":
                            string times = XpathUtil.GetText(hn, kvp.Value.text);
                            time = RegexUtil.MatchText(times, @"[\d]+-[\d]+-[\d]+ [\d]+:[\d]+:[\d]+");
                            break;
                        case "author":
                            author = XpathUtil.GetText(hn, kvp.Value.text);
                            break;
                        case "content":
                            content = XpathUtil.GetTexts(hn, kvp.Value.text, false, "");
                            break;
                    }
                }
                textEntity.title = title;
                textEntity.time = DateTime.Parse(time);
                textEntity.author = author;
                textEntity.content = RegexUtil.RemoveNoise(content, "&nbsp;|●|\t|\r|\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }
        }
    }
}
