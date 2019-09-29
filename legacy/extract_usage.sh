outfile=$(mktemp -t "usage_tsudo.XXXXXXX")

"$PYTHONUSERBASE"/bin/excode -f 'shell,tsu' README.md $outfile

sed -i'' -e '1d;$d' $outfile 

OUTFILE="$outfile" perl -e 'open my $S, "<", "$ENV{OUTFILE}" or die $!;
         $salt = do { local $/ ; <$S> };
         s/#SHOW_USAGE_BLOCK/$salt/, print while <>;
        ' src/tsu.sh > bin/tsu

