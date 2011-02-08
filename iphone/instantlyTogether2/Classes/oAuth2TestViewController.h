//
//  oAuth2TestViewController.h
//  oAuth2Test
//
//  Created by dominic dimarco on 5/22/10.
//  Copyright 214Apps 2010. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "oAuth2TestAppDelegate.h"
#import "oAuth2TestViewController.h"

@class FreeFriendsViewController;

@interface oAuth2TestViewController : UIViewController <UIWebViewDelegate> {

	IBOutlet UIWebView *webView;
	FreeFriendsViewController* freeViewController;
	NSMutableData *responseData;
	
	
}
@property (nonatomic, retain) UIWebView *webView;
@property (nonatomic, retain) FreeFriendsViewController *freeViewController;
@end

