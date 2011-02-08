//
//  oAuth2TestViewController.m
//  oAuth2Test
//
//  Created by dominic dimarco on 5/22/10.
//  Copyright 214Apps 2010. All rights reserved.
//

#import "oAuth2TestViewController.h"
#import "oAuth2TestAppDelegate.h"
#import "FreeFriendsViewController.h"

#import "JSON/JSON.h"
@implementation oAuth2TestViewController

@synthesize webView;
@synthesize freeViewController;

// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
	
    [super viewDidLoad];
	
	/*Facebook Application ID*/
	NSString *client_id = @"125675287489480";
	
	/*Dummy page hosted by the nice folks at Facebook*/
	NSString *redirect_uri = @"http://www.facebook.com/connect/login_success.html";
	
	NSString *url_string = [NSString stringWithFormat:@"https://graph.facebook.com/oauth/authorize?client_id=%@&redirect_uri=%@&type=user_agent&display=touch", client_id, redirect_uri];
	
	NSURL *url = [NSURL URLWithString:url_string];
	NSURLRequest *request = [NSURLRequest requestWithURL:url];
	[self.webView loadRequest:request];
	NSLog(@"view loaded");
}

- (void)webViewDidFinishLoad:(UIWebView *)_webView {
	
	/**
	 * Since there's some server side redirecting involved, this method/function will be called several times
	 * we're only interested when we see a url like:  http://www.facebook.com/connect/login_success.html#access_token=..........
	 */
	
	//get the url string
	NSString *url_string = [((_webView.request).URL) absoluteString];
	
	//looking for "access_token="
	NSRange access_token_range = [url_string rangeOfString:@"access_token="];
	
	//coolio, we have a token, now let's parse it out....
	if (access_token_range.length > 0) {
		
		//we want everything after the 'access_token=' thus the position where it starts + it's length
		int from_index = access_token_range.location + access_token_range.length;
		NSString *access_token = [url_string substringFromIndex:from_index];
		

		
		responseData = [[NSMutableData data] retain];
		
		NSString * requestURL = [NSString stringWithFormat:@"http://instantlytogether.appspot.com/whose_free.json?access_token=%@", access_token];
		NSLog(@"URL::%@", requestURL);
		NSURL *url =[NSURL URLWithString:requestURL];

		NSURLRequest *request = [[NSURLRequest alloc] initWithURL:url];
		NSURLConnection *connection =[[NSURLConnection alloc] initWithRequest:request delegate:self];
		[connection release];
		[request release];

	}
}
	
- (void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data 
{
	// Store incoming data into a string
	NSString *jsonString = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
	SBJSON *parser = [SBJSON new];
	NSLog(@"STRING::%@", jsonString);
	NSDictionary *results = [parser objectWithString:jsonString];
	NSLog(@"members of Data%@", [[results valueForKey:@"data"] valueForKey:@"name"]);
	NSMutableArray *names = [[results valueForKey:@"data"] valueForKey:@"name"];
	NSMutableArray *ids = [[results valueForKey:@"data"] valueForKey:@"id"];
	NSMutableArray *times = [[results valueForKey:@"data"] valueForKey:@"last_time"];
	
	[self.webView stopLoading];
	oAuth2TestAppDelegate *delegate = (oAuth2TestAppDelegate*)[[UIApplication sharedApplication] delegate];
	FreeFriendsViewController *freeView = [[FreeFriendsViewController alloc] initWithNibName:@"FreeFriendsView" bundle:[NSBundle mainBundle]];
	freeView.names = names;
	freeView.ids = ids;
	freeView.times = times;
	[delegate.navController presentModalViewController:freeView animated:YES];
	[freeView release];
	delegate=nil;
	

}
	

- (void)dealloc {
	[webView release];
    [super dealloc];
}



@end
